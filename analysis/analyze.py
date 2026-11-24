"""Locked paired exact tests and Holm adjustment for completed BT-EXP-001."""
import csv
import json
import math
import sys
from pathlib import Path

COUPLINGS = (.5, 1., 2., 4., 8.)
NOISES = (0., .2, .5)
SEEDS = set(range(30))

def sign_test_p(positive, negative):
    n = positive + negative
    if n == 0:
        return 1.
    return sum(math.comb(n, k) for k in range(positive, n + 1)) / (2 ** n)

def holm_adjust(pvalues):
    order = sorted(range(len(pvalues)), key=lambda i: pvalues[i])
    adjusted = [1.] * len(pvalues)
    previous = 0.
    for rank, idx in enumerate(order):
        previous = max(previous, min(1., (len(pvalues) - rank) * pvalues[idx]))
        adjusted[idx] = previous
    return adjusted

def analyze(path: Path):
    with path.open(newline="") as file:
        raw = list(csv.DictReader(file))
    records = {}
    for row in raw:
        key = (int(row["seed"]), float(row["coupling"]), float(row["noise"]))
        if key in records:
            raise ValueError("Duplicate experiment row")
        records[key] = row["multi_domain_success"].lower() == "true"
    expected = {(seed, k, sigma) for seed in SEEDS for sigma in NOISES for k in (0.,) + COUPLINGS}
    if set(records) != expected:
        raise ValueError("Missing or extra experiment rows")
    results = []
    for sigma in NOISES:
        for k in COUPLINGS:
            up = sum(records[(seed, k, sigma)] and not records[(seed, 0., sigma)] for seed in SEEDS)
            down = sum(not records[(seed, k, sigma)] and records[(seed, 0., sigma)] for seed in SEEDS)
            rate = sum(records[(seed, k, sigma)] for seed in SEEDS) / 30
            baseline = sum(records[(seed, 0., sigma)] for seed in SEEDS) / 30
            results.append({"coupling": k, "noise": sigma, "success_rate": rate,
                "baseline_rate": baseline, "paired_difference": rate - baseline,
                "positive_discordances": up, "negative_discordances": down,
                "raw_p": sign_test_p(up, down)})
    adjusted = holm_adjust([item["raw_p"] for item in results])
    for item, p in zip(results, adjusted):
        item["holm_p"] = p
        item["significant"] = bool(item["paired_difference"] > 0 and p < .05)
    return {"n_trajectories": len(records), "alpha": .05,
            "any_primary_support": any(x["significant"] for x in results), "comparisons": results}

if __name__ == "__main__":
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "results/summary.csv")
    print(json.dumps(analyze(path), indent=2))
