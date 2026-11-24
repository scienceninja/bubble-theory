# OF-F01 — Observation Foam: Formal Framework v0.1

Date: 2026-11-23. Status: proposed mathematical framework, NOT established quantum physics.

## Research question
Can the geometry of lower-dimensional membranes between observer-associated domains yield useful mathematical models of observation, ownership, interactions, and higher-dimensional structure?

## Epistemic layers
1. Established geometry: Voronoi / power partitions and equilibrium surfaces.
2. Proposed dynamics: ownership inventory, surface tension, exchange, anchors and topology change.
3. Speculative interpretation: quantum ownership and higher-dimensional physical reality. No implication from 1 or 2 to 3 is assumed.

## Primitives
- observation event o_i in spacetime
- spatial anchor a_i(t)
- discrete inventory n_i = (n_i1,...,n_ik)
- domain B_i(t)
- shared membrane M_ij = boundary(B_i) intersection boundary(B_j)
- effective tension gamma_ij
- active status

## Proposed axioms
A1: Admitted observation events generate candidate domain labels and anchors.
A2: Active domains have pairwise disjoint interiors in a selected spatial slice.
A3: Adjacent domains share a single geometric interface.
A4: Inventories constrain preferred domain measures and interface energies via explicit functions.
A5: Local prescribed dynamics govern formation, exchange, merger and collapse.
A6: A higher-dimensional embedding is an optional modeling choice, not assumed physical fact.

## Exact baseline: point-generated partition
For anchors a_i in a bounded Euclidean region Omega,
B_i = {x in Omega: ||x-a_i||^2 <= ||x-a_j||^2 for all j}.
The equal-distance boundary between i and j obeys
2 x dot (a_j-a_i) = ||a_j||^2 - ||a_i||^2.
Therefore boundaries between ordinary Voronoi cells are contained in affine hyperplanes (subject to competition with other anchors and the enclosing domain).

Weighted power baseline:
B_i = {x: ||x-a_i||^2 - w_i <= ||x-a_j||^2 - w_j for all j}.
Boundaries remain affine hyperplanes even when w_i differ. Weights do not automatically produce curvature; cells may be empty.

## Energy-based foam alternative
E = sum_{i<j} gamma_ij * Area(M_ij)
  + sum_i (k_i/2) * [Vol(B_i)-V_i*(n_i)]^2
subject to domain partition and explicit anchor constraints.
gamma_ij and V_i*(n_i) are model functions, not physically established quantum quantities.

Young-Laplace in 3D: Delta P = 2 gamma H, H mean curvature. Delta P=0 implies H=0, but NOT necessarily a planar interface: catenoids and other minimal surfaces are counterexamples. Balanced symmetric planar interfaces are a special case, not a universal axiom.

## Time, observation and identity
An observation is modeled as a discrete event; events from a persistent observer may or may not share a label. A spacetime event is distinct from a persistent worldline. A continuum of observation events requires a different mathematical description and is not assumed.

## Transformations and open definitions
Formation: add anchor and recompute partition/energy minimizer.
Exchange: transfer discrete inventory between adjacent cells, conserving specified quantities.
Merger: remove interface, specify fate of both anchors separately.
Collapse: deactivate anchor and redistribute territory; no resource loss without explicit law.

## Critical limitations
- Exclusive geometric ownership is NOT a standard property of entangled quantum systems.
- No quantum state, Hilbert space, measurement instrument, causality rule, or Born probabilities are defined here.
- Observation-generated geometry does not demonstrate physical spacetime emergence.
- Higher-dimensional embedding alone does not generate new experimental predictions.
- A constrained model can match foam behavior by construction; meaningful research requires novel consequences and alternate models.

## First toy experiment OF-EXP-001 (exploratory)
On a bounded 2D region:
1. Specify a finite set of points with fixed random seeds.
2. Generate ordinary Voronoi cells; verify nonoverlap, coverage and flat interfaces.
3. Add weights via power diagram; verify translated but still flat interfaces, and report empty cells.
4. Implement an independent area/perimeter minimization model using composition-dependent gamma_ij and preferred areas.
5. Compare shapes, junctions, area distribution and topology changes across models.
6. Perform event insertion/removal and resource exchange with defined conservation.
7. Only then attempt extension to 3D cells / 2D membranes and 4D cells / 3D membranes.

## Falsification / evaluation
This is currently a formal modeling proposal, not a falsifiable quantum hypothesis. To become physical theory, ownership must be operationally defined and predictions must distinguish the framework from established quantum mechanics and relativity. All negative cases and baseline equivalences are required.

Related research: BT-F01 and BT-EXP-001 oscillators are a separate exploratory program, neither invalidated nor validated by OF-F01.
