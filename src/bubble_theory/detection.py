"""Read-only domain detection independent of the simulation."""
from dataclasses import dataclass
import numpy as np
from .engine import ring_neighbors

@dataclass(frozen=True)
class DetectionConfig:
    edge_threshold: float = 0.85
    min_size: int = 4
    max_size: int = 64
    internal_threshold: float = 0.80
    distinction_threshold: float = 0.20
    persistence_windows: int = 4
    persistence_min_pass: int = 3

def edges_for_ring(n: int, radius: int):
    neighbors = ring_neighbors(n, radius)
    return np.array(sorted({tuple(sorted((i, int(j)))) for i in range(n) for j in neighbors[i]}), dtype=int)

def phase_locking(path, edges):
    if len(path) == 0:
        raise ValueError("Empty observation window")
    difference = path[:, edges[:, 0]] - path[:, edges[:, 1]]
    return np.abs(np.exp(1j * difference).mean(axis=0))

def candidates(path, edges, cfg: DetectionConfig = DetectionConfig()):
    n = path.shape[1]
    plv = phase_locking(path, edges)
    parent = list(range(n))
    def root(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for (a, b), value in zip(edges, plv):
        if value >= cfg.edge_threshold:
            x, y = root(int(a)), root(int(b))
            if x != y:
                parent[y] = x
    groups = {}
    for node in range(n):
        groups.setdefault(root(node), []).append(node)
    return sorted((tuple(g) for g in groups.values() if cfg.min_size <= len(g) <= cfg.max_size), key=lambda x: x[0])

def scores(path, edges, group):
    inside = np.zeros(path.shape[1], dtype=bool)
    inside[list(group)] = True
    a, b = edges[:, 0], edges[:, 1]
    inner = inside[a] & inside[b]
    boundary = inside[a] ^ inside[b]
    if not inner.any() or not boundary.any():
        return float("nan"), float("nan")
    plv = phase_locking(path, edges)
    mean = float(plv[inner].mean())
    return mean, float(mean - plv[boundary].mean())

def validate(path, edges, group, cfg: DetectionConfig = DetectionConfig()):
    inner, difference = scores(path, edges, group)
    subpasses = []
    for window in np.array_split(path, cfg.persistence_windows):
        a, b = scores(window, edges, group)
        subpasses.append(bool(a >= cfg.internal_threshold and b >= cfg.distinction_threshold))
    valid = bool(inner >= cfg.internal_threshold and difference >= cfg.distinction_threshold
                 and sum(subpasses) >= cfg.persistence_min_pass)
    return {"nodes": list(group), "internal_plv": inner, "distinction": difference,
            "subwindow_passes": subpasses, "validated": valid}

def evaluate(path, config_dt, n, radius, cfg: DetectionConfig = DetectionConfig()):
    """Discovery [100,150), validation [150,200). No validation-driven relabeling."""
    def window(a, b):
        x, y = round(a / config_dt), round(b / config_dt)
        if abs(x * config_dt - a) > 1e-7 or abs(y * config_dt - b) > 1e-7:
            raise ValueError("Unaligned measurement window")
        if len(path) < y:
            raise ValueError("Trajectory too short")
        return path[x:y]
    edges = edges_for_ring(n, radius)
    found = candidates(window(100, 150), edges, cfg)
    checked = [validate(window(150, 200), edges, g, cfg) for g in found]
    count = sum(v["validated"] for v in checked)
    return {"candidate_count": len(found), "validated_count": count,
            "multi_domain_success": bool(count >= 2), "domains": checked}
