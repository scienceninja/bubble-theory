# BT-EXP-001 Preregistration Draft

Status: DRAFT, NOT publicly registered, NOT executed. Do not interpret diagnostic code runs as scientific confirmation.

## Primary hypothesis
For some positive coupling K, the seed-paired probability of at least two validated domains exceeds K=0 for the same noise sigma.

## Fixed simulation
128 nodes on an undirected radius-4 periodic ring. Noisy local Kuramoto dynamics:
dtheta_i = [omega_i+(K/8)*sum_{j neighbor i} sin(theta_j-theta_i)]dt + sigma*dW_i.
omega iid N(0,1), initial phase iid Uniform(0,2pi).
Seeds 0-29; K 0,.5,1,2,4,8; sigma 0,.2,.5; dt .02; total time 250.
Euler-Maruyama; standard normal innovations shared across K and sigma for each seed.
540 trajectories.

## Temporal windows
Burn-in [0,100), discovery [100,150), validation [150,200), follow-up [200,250).
Half-open intervals sampled at k*dt.

## Candidate detection
PLV on graph edges in discovery window. Keep edges PLV >=.85.
Connected components of 4-64 nodes are candidates. Freeze membership.

## Validation
Full validation window internal PLV >=.80 and distinction >=.20.
Both thresholds pass in at least 3 of four consecutive 12.5-time-unit subwindows.
At least two validated candidates yields success.

## Statistical analysis
For each of 15 positive-K versus matched K=0 comparisons use exact one-sided paired sign test on discordant outcomes. Holm adjusted familywise alpha=.05.
Report all 18 condition rates and negative outcomes. No power sufficiency claimed.

## Exploratory controls
All-to-all coupling, circular-shift temporal surrogates, degree-preserving rewiring.

## Remaining prerequisites
Freeze exact runtime/NumPy/BLAS environment; numeric tolerances; RNG streams; result provenance and archival plan. Timestamp public preregistration BEFORE registered execution.
