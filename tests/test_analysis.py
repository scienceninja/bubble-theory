import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from analyze import sign_test_p, holm_adjust

def test_one_sided_exact_test():
    assert sign_test_p(0, 0) == 1
    assert sign_test_p(5, 0) == 1 / 32
    assert sign_test_p(0, 5) == 1

def test_holm_monotonic():
    values = holm_adjust([.04, .001, .03])
    assert values[1] == .003
    assert values[2] <= values[0]
