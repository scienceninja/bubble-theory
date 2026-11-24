import numpy as np
from bubble_theory.detection import edges_for_ring, phase_locking, candidates, evaluate, DetectionConfig

def test_edges_unique():
    edges = edges_for_ring(16, 2)
    assert edges.shape == (32, 2)
    assert np.all(edges[:, 0] < edges[:, 1])

def test_phase_locking_perfect_for_fixed_relative_phase():
    t = np.linspace(0, 9, 100)
    path = np.column_stack((t, t + .7, t + 2))
    assert np.allclose(phase_locking(path, np.array([[0, 1], [1, 2]])), 1)

def test_no_domains_on_uniform_global_coherence():
    t = np.linspace(0, 8, 3000)
    path = np.tile(t[:, None], (1, 32))
    assert candidates(path, edges_for_ring(32, 2), DetectionConfig(max_size=16)) == []

def test_holdout_is_not_discovery_data():
    n, dt, steps = 16, .02, 10000
    rng = np.random.default_rng(123)
    path = rng.uniform(0, 2 * np.pi, (steps, n))
    t = np.arange(steps) * dt
    for j in range(4, 10):
        path[5000:7500, j] = np.mod(t[5000:7500], 2 * np.pi)
    found = candidates(path[5000:7500], edges_for_ring(n, 1), DetectionConfig(max_size=12))
    assert any(set(range(4, 10)).issubset(set(g)) for g in found)
    assert evaluate(path, dt, n, 1, DetectionConfig(max_size=12))["validated_count"] == 0
