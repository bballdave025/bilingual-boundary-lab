import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("experiment", Path(__file__).resolve().parents[1] / "scripts/run_first_experiment.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_prefix_keeps_one_more_run_than_switches():
    assert module.select_prefix([1, 2, 3, 4], 2) == [1, 2, 3], "Two switches need three complete runs."


def test_zero_changes_keeps_first_run():
    assert module.select_prefix([1, 2], 0) == [1], "Zero switches still includes the first run."


def test_short_corpus_warns_without_failing(capsys):
    assert module.select_prefix([1, 2], 1000) == [1, 2], "A short corpus must remain usable."
    assert "only 1" in capsys.readouterr().err, "Explain how many transitions were available."


def test_default_preserves_all_runs():
    assert module.select_prefix([1, 2], None) == [1, 2]


def test_negative_request_is_rejected():
    with pytest.raises(ValueError, match="nonnegative"):
        module.select_prefix([1], -1)
