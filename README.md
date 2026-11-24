# Bubble Theory Research Engine

BT-F01 v1.0 / BT-EXP-001. A bubble-free oscillator universe and independent coherent-domain detector.

Setup:
    python -m pip install -e '.[test]'
    python -m pytest -q
    bubble-theory --mode diagnostic --output results

Do NOT run the 540-run registered experiment before externally timestamping and freezing the protocol. No confirmatory results exist.

After public registration, use an EMPTY output directory and run:

    bubble-theory --mode registered --output results/registered-001 --registration-id <permanent-registration-identifier> --confirm-registered
    python analysis/analyze.py results/registered-001/summary.csv

Registered mode refuses to start without a registration identifier and an explicit acknowledgement. This is a procedural safeguard, not external verification of registration.
Experiment outputs include environment and source-file SHA-256 metadata.

Six commitments: no prescribed bubbles; no preferred outcome; no circular validation; no automatic physics claims; no assumed novelty; reproducibility.

See foundations/BT-F01.md and preregistrations/BT-EXP-001.md.
