"""Diagnostic runner and fixed BT-EXP-001 batch execution."""
import argparse
import csv
import hashlib
import json
import platform
import sys
from pathlib import Path
import numpy as np
from .engine import SimulationConfig, simulate
from .detection import evaluate

REGIMES = [(k, s) for s in (0., .2, .5) for k in (0., .5, 1., 2., 4., 8.)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("diagnostic", "registered"), default="diagnostic")
    parser.add_argument("--registration-id", help="Permanent public registration identifier for confirmatory runs")
    parser.add_argument("--confirm-registered", action="store_true", help="Acknowledge frozen preregistration")
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
    if not args.confirm_registered or not args.registration_id or not args.registration_id.strip():
        parser.error("registered mode requires --confirm-registered and --registration-id after external preregistration")
    if any(out.iterdir()):
        parser.error("registered mode requires an empty output directory; never overwrite existing runs")
    config = SimulationConfig()
    run_metadata = {"registration_id": args.registration_id.strip(), "python": sys.version,
                    "platform": platform.platform(), "numpy": np.__version__,
                    "config": vars(config), "regimes": REGIMES, "seeds": list(range(30)),
                    "integration": "Euler-Maruyama", "float_type": "float64",
                    "rng": "numpy.default_rng / PCG64 via SeedSequence([seed,stream])",
                    "time_windows": [[0,100],[100,150],[150,200],[200,250]]}
    (out / "run_metadata.json").write_text(json.dumps(run_metadata, indent=2) + "\n")
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
