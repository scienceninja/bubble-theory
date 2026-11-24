"""Exploratory 36-run sweep; NOT part of confirmatory BT-EXP-001.

Usage: python discovery/explore_001.py --output discovery/output
Requires installed bubble_theory, numpy.
"""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from bubble_theory.engine import SimulationConfig, simulate
from bubble_theory.detection import evaluate, edges_for_ring, phase_locking

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="discovery/output")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    cfg = SimulationConfig()
    edges = edges_for_ring(cfg.n, cfg.radius)
    rows = []
    for seed in (0, 1, 2):
        for noise in (0., .2):
            for coupling in (0., .5, 1., 2., 4., 8.):
                path = simulate(seed, coupling, noise, cfg)
                result = evaluate(path, cfg.dt, cfg.n, cfg.radius)
                discovery = phase_locking(path[5000:7500], edges)
                validation = phase_locking(path[7500:10000], edges)
                rows.append({
                    "seed": seed, "sigma": noise, "K": coupling,
                    "success": result["multi_domain_success"],
                    "candidates": result["candidate_count"],
                    "validated": result["validated_count"],
                    "discover_mean_edge_plv": float(discovery.mean()),
                    "validation_mean_edge_plv": float(validation.mean()),
                    "discover_fraction_strong": float((discovery >= .85).mean())
                })
                print(f"seed={seed} sigma={noise} K={coupling} validated={result['validated_count']}")
    with (out / "raw.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (out / "raw.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(f"Saved {len(rows)} exploratory runs")

if __name__ == "__main__":
    main()
