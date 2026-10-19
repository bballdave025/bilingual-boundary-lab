from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bbl.anomalies import find_mixed_script_tokens
from bbl.ngram import NGramModel
from bbl.normalization import (
    normalized_character_stream,
    normalized_tokens,
)
from bbl.runs import build_runs
from bbl.visualization import log_radius, plot_runs

CORPUS_PATH = (
    REPO_ROOT / "data/raw/war_and_peace_ru_fr_wikisource.txt"
)
RUNS_PATH = REPO_ROOT / "data/processed/script_runs.json"
FIGURE_PATH = REPO_ROOT / "outputs/figures/script_runs_base10.png"
SUMMARY_PATH = REPO_ROOT / "outputs/first_experiment_summary.json"


def select_prefix(runs, num_changes):
    """Keep complete runs: N class switches require N + 1 runs."""
    if num_changes is None:
        return runs
    if num_changes < 0:
        raise ValueError("number of changes must be nonnegative")
    available = max(0, len(runs) - 1)
    if num_changes > available:
        print(
            f"Warning: requested {num_changes} script-class changes, "
            f"but only {available} are available; plotting all runs.",
            file=sys.stderr,
        )
    return runs[:num_changes + 1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the initial corpus experiment.")
    parser.add_argument(
        "--num-language-changes", type=int, default=None, metavar="TARGET_NUMBER",
        help="Plot the first N script-class changes (N+1 complete runs). "
             "Includes numeric/other transitions; not inferred language identity.",
    )
    args = parser.parse_args()
    if args.num_language_changes is not None and args.num_language_changes < 0:
        parser.error("--num-language-changes must be nonnegative")
    text = CORPUS_PATH.read_text(encoding="utf-8")
    words = normalized_tokens(text)
    characters = normalized_character_stream(text)
    runs = build_runs(text)
    anomalies = find_mixed_script_tokens(text)

    RUNS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNS_PATH.write_text(
        json.dumps(
            [run.as_pair() for run in runs],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    plotted_runs = select_prefix(runs, args.num_language_changes)
    figure_path = FIGURE_PATH if args.num_language_changes is None else (
        FIGURE_PATH.with_name(
            f"script_runs_base10_first_{args.num_language_changes}_changes.png"
        )
    )
    plot_runs(
        plotted_runs,
        figure_path,
        base=10,
        radius_limit=max((log_radius(r.length) for r in runs), default=0),
    )

    samples: dict[str, str] = {}
    model_stats: dict[str, dict[str, int]] = {}

    for n in (0, 1, 2, 3):
        word_model = NGramModel[str](n).fit(words)
        word_sample = word_model.generate(
            100,
            seed=words[:n],
            random_seed=1729 + n,
        )
        samples[f"word_n{n}"] = " ".join(word_sample)
        model_stats[f"word_n{n}"] = {
            "contexts": word_model.training_context_count(),
            "vocabulary": len(word_model.vocabulary),
        }

    for n in (0, 1, 2, 3, 5):
        char_model = NGramModel[str](n).fit(characters)
        char_sample = char_model.generate(
            500,
            seed=characters[:n],
            random_seed=2718 + n,
        )
        samples[f"character_n{n}"] = "".join(char_sample)
        model_stats[f"character_n{n}"] = {
            "contexts": char_model.training_context_count(),
            "vocabulary": len(char_model.vocabulary),
        }

    summary = {
        "corpus_characters": len(text),
        "normalized_words": len(words),
        "normalized_characters": len(characters),
        "run_count": len(runs),
        "run_classes": Counter(
            run.script.name for run in runs
        ),
        "mixed_script_token_count": len(anomalies),
        "mixed_script_examples": [
            {
                "token": finding.token,
                "scripts": finding.scripts,
            }
            for finding in anomalies[:50]
        ],
        "models": model_stats,
        "samples": samples,
    }

    SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {RUNS_PATH}")
    print(f"Wrote {figure_path} ({len(plotted_runs)} runs)")
    print(f"Wrote {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
