"""Safety check: confirmatory mode cannot start accidentally."""
import sys
import pytest
from bubble_theory.cli import main

def test_registered_mode_requires_external_registration_ack(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["bubble-theory", "--mode", "registered",
                                      "--output", str(tmp_path / "study")])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert not (tmp_path / "study" / "run_metadata.json").exists()

def test_registered_mode_requires_identifier(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["bubble-theory", "--mode", "registered",
                                      "--confirm-registered", "--output", str(tmp_path / "study")])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
