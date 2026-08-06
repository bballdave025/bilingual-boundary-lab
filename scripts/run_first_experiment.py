from __future__ import annotations

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
from bbl.visualization import plot_runs

CORPUS_PATH = (
    REPO_ROOT / "data/raw/war_and_peace_ru_fr_wikisource.txt"
)
RUNS_PATH = REPO_ROOT / "data/processed/script_runs.json"
FIGURE_PATH = REPO_ROOT / "outputs/figures/script_runs_base10.png"
SUMMARY_PATH = REPO_ROOT / "outputs/first_experiment_summary.json"


def main() -> None:
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

    plot_runs(
        runs,
        FIGURE_PATH,
        base=10,
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
    print(f"Wrote {FIGURE_PATH}")
    print(f"Wrote {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
