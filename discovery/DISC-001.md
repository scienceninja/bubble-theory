# DISC-001: Local oscillator exploratory sweep

**Date:** 2026-11-23. **Status:** exploratory, not preregistered, not confirmatory.
Engine: existing Bubble Theory Euler–Maruyama local Kuramoto model; n=128; radius=4; dt=.02; duration=250. Seeds 0, 1, 2. K=0,.5,1,2,4,8; sigma=0,.2. Discovery [100,150), validation [150,200); fixed BT-EXP-001 detection thresholds. 36 simulations. Python local execution with NumPy 2.3.5; source based on initial v0.1 engine. The full 540-run confirmatory study has **not** been executed.

| Noise sigma | Coupling K | Runs with >=2 validated domains | Mean validated domains | Mean validation-edge PLV | Discovery-edge fraction >=0.85 |
|---:|---:|---:|---:|---:|---:|
|0|0|0/3|0|0.075|0.020|
|0|0.5|3/3|3.00|0.206|0.090|
|0|1|3/3|7.67|0.397|0.200|
|0|2|3/3|7.00|0.811|0.643|
|0|4|0/3|0|0.993|0.985|
|0|8|0/3|0|1.000|1.000|
|0.2|0|0/3|0|0.096|0.007|
|0.2|0.5|0/3|1.00|0.195|0.041|
|0.2|1|3/3|5.33|0.381|0.142|
|0.2|2|3/3|6.33|0.796|0.610|
|0.2|4|0/3|0|0.986|0.984|
|0.2|8|0/3|0|0.997|1.000|

## Initial interpretation
Intermediate coupling permits differentiated coherent components with measurable persistence on held-out time windows. High coupling yields nearly all ring edges strongly phase locked and a near-global coherent network; the *detector* then returns no proper 4–64-node components. This is **not evidence that coherence disappears**; rather domain *differentiation* disappears under the selected operational definition. At K=0 the detector identifies no domains.

## Caveats
- Three seeds per cell: very small exploratory sample, no statistical claim.
- A local ring and a connected-component thresholding detector can generate apparent localized communities. Existence is not novel.
- Size upper limit 64 structurally excludes a single global component. That is intentional for differentiation, but limits interpretation.
- Phase locking is not equivalent to causal independence, individuality, or emergent geometry.
- No all-to-all, surrogate, rewiring, perturbation or hierarchical test completed in this exploration.
- All numeric results are descriptive; do not mix with future confirmatory data.

## Reproduce
Run `python discovery/explore_001.py --output discovery/output` from an environment with the package installed. Original raw output is available in the conversation artifact; repo script generates the same core columns from the committed engine.

## Next research priorities
1. Test whether domain identity survives perturbations and constituent replacement.
2. Compare with known community detection and stationary graph structure.
3. Test hierarchy using out-of-sample predictive benefits rather than nested clusters alone.
