"""Diagnostic runner and fixed BT-EXP-001 batch execution."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from .engine import SimulationConfig, simulate
from .detection import evaluate

REGIMES = [(k, s) for s in (0., .2, .5) for k in (0., .5, 1., 2., 4., 8.)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("diagnostic", "registered"), default="diagnostic")
    parser.add_argument("--output", default="results")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--coupling", type=float, default=2.)
    parser.add_argument("--noise", type=float, default=.2)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    if args.mode == "diagnostic":
        config = SimulationConfig(n=32, radius=2, dt=.02, duration=10.)
        phases = simulate(args.seed, args.coupling, args.noise, config)
        dest = out / "diagnostic.npz"
        np.savez_compressed(dest, t=np.arange(len(phases)) * config.dt, phases=phases)
        print(json.dumps({"status": "diagnostic-only", "shape": phases.shape, "file": str(dest)}))
        return
    config = SimulationConfig()
    rows = []
    for seed in range(30):
        for coupling, noise in REGIMES:
            phases = simulate(seed, coupling, noise, config)
            result = evaluate(phases, config.dt, config.n, config.radius)
            name = f"seed{seed:02d}_k{coupling:g}_sigma{noise:g}.json"
            payload = {"seed": seed, "coupling": coupling, "noise": noise, "simulation": vars(config), **result}
            (out / name).write_text(json.dumps(payload, indent=2) + "\n")
            rows.append({key: payload[key] for key in ("seed", "coupling", "noise",
                        "candidate_count", "validated_count", "multi_domain_success")})
            print(name, flush=True)
    with (out / "summary.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(out.iterdir()) if p.is_file() and p.name != "sha256.json"}
    (out / "sha256.json").write_text(json.dumps(manifest, indent=2) + "\n")

if __name__ == "__main__":
    main()
