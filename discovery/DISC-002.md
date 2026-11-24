# DISC-002 — Coherent-domain resilience under phase disturbance

**Date:** 2026-11-23. **Status:** EXPLORATORY. Not a preregistered test, not a mathematical proof, and not new physics.

## Question
Does a detected coherent region retain its phase-locking distinction after a sudden intervention that shifts half its constituent oscillator phases by pi radians?

## Protocol
Fixed undirected 128-node radius-4 ring; local noisy Kuramoto dynamics; Euler–Maruyama dt=.02. Three seeds (0–2), K in {1,2}, sigma in {0,.2}: **12 starting trajectories**. Detect domains using only phase data from [100,150); select largest eligible component, breaking ties lexicographically. At t=150 branch into:
- **Sham:** no intervention.
- **Within-domain:** phase kick of pi on randomly selected ceiling(size/2) internal nodes.
- **Outside-domain:** same-sized phase kick on nodes outside the target.

Branch trajectories receive *identical subsequent Brownian innovations* and keep the original parameters. Selection RNG uses SeedSequence([seed, int(K*10), int(sigma*10), 202]). Compare internal PLV and boundary distinction on [150,160) and [190,200). One unit of analysis is a matched trajectory trio, **not** each oscillator.

## Aggregate descriptive outcomes (12 trios)

| Condition | Early mean internal PLV | Early mean distinction | Late mean internal PLV | Late mean distinction |
|---|---:|---:|---:|---:|
| Sham | 0.961 | 0.507 | 0.947 | 0.444 |
| Within-domain kick | 0.757 | 0.266 | 0.958 | 0.436 |
| Outside-domain kick | 0.954 | 0.496 | 0.936 | 0.448 |

Paired within-domain minus sham distinction: **-0.241 early**, **-0.008 late**.
Paired outside-domain minus sham distinction: **-0.012 early**, **+0.004 late**.

In the late window, **10 of 12** target domains in each branch exceeded the original full-window thresholds of internal PLV >=.8 and distinction >=.2. All 12 within-domain kicked groups had positive late distinction, but this alone is a weak criterion.

## Interpretation
Within-domain phase shocks temporarily degrade the target's phase-locking advantage. By [190,200), the *average* difference from an unperturbed continuation is small. Some individual trajectories are substantially different, so this is **consistent with partial or heterogeneous recovery**, not evidence that every domain restores a distinct independent identity.

This experiment retains fixed membership. It **does not test constituent replacement, persistence of membership boundaries, autonomy, causal individuality, hierarchical emergence or novel physical principles**. The ring topology and local dynamics may explain all observations; no graph-only or alternative coupling comparisons have yet been completed.

## Limitations
- Just 12 target domain trios, hand-selected exploratory parameter window already informed by DISC-001; no inferential p-values.
- A fixed domain and late coherence are not enough to show recovery to the *same state*. Phase-locking ignores constant relative phase offsets.
- A disturbance outside the target can still reach it via graph links.
- The target's baseline may evolve even without intervention (late sham distinction sometimes falls below .2).
- Perturbation size differs with selected domain size (observed range 5–55 nodes).
- No membership rewiring, replacement, or causal independence assay.

## Reproducibility
Execute `python discovery/disc_002.py` using the repository package. Output includes raw JSON/CSV. The underlying 14-test engine suite passed locally before this study; the GitHub script itself requires CI execution/verification. A raw artifact bundle is attached in the conversation.

## Next: DISC-003
A more defensible individuality assay should measure **state recovery, boundary survival under membership turnover, and incremental predictive value** against static graph community baselines. Add explicit similarity to the unperturbed path and matched perturbation-distance controls.
