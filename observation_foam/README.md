# Observation Foam / OF-EXP-001

Exploratory geometric model only; no claims about quantum observation or spacetime.

Each observation anchor generates a cell of a **power diagram**. Cells have disjoint interiors and shared flat boundaries. An inventory of discrete owned units gives target relative cell areas. A deterministic iterative solver adjusts the additive power weights until the approximate sampled areas approach the targets.

The separate Python reference implementation, tests and reproducible study are in this directory. An interactive standalone browser prototype is included under web/index.html.

Run Python tests using:
    PYTHONPATH=observation_foam/src python -m pytest observation_foam/tests -q

Run experiment from repo root:
    PYTHONPATH=observation_foam/src python observation_foam/experiments/run_of001.py

Cautions: power diagrams have affine interfaces by construction; inventory-based weights are NOT physical surface tension. No curvature, actual membrane relaxation, quantum information, or higher-dimensional physics has been implemented yet.