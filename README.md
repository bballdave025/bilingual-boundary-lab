# Bilingual Boundary Lab

A visualization-first experiment in what simple statistical language models
can learn from one bilingual literary corpus: Tolstoy's *War and Peace* in
Russian with its original French passages.

## Research question

How far can deliberately simple models get when trained only on one novel,
especially around language switching, boundary persistence, and memorization?

## Model Order 0

This project intentionally uses:

- no external corpus;
- no pretrained language detector;
- no transformer;
- no automatic translation;
- no corpus augmentation.

The first model family is an `n`-parameterized n-gram model for characters
and words. Here, `n` is the number of tokens in the conditioning context.
Thus `n=0` is an unconditional frequency model, `n=1` is the familiar
first-order Markov form, and so on.

## Canonical visualization

Each maximal script run is exactly one vertical column.

- Horizontal position: run order, not character position.
- Color: Cyrillic, Latin, numeric, or other.
- Symmetric vertical radius: rounded logarithm of run length.

For base `b`, the displayed radius is

```text
floor(log_b(run_length) + 0.5)
```

so boundaries occur at geometric means `b ** (k + 1/2)`.

The logarithm base is an experimental visualization parameter rather than a
mathematically sacred choice. It should be selected for human-readable
information density.

## Reproducible corpus

The corpus builder is:

```text
scripts/build_war_and_peace_corpus.py
```

Its default output is:

```text
data/raw/war_and_peace_ru_fr_wikisource.txt
```

Run:

```bash
python scripts/build_war_and_peace_corpus.py
```

The generated corpus is included in this ZIP when network access allowed the
builder to complete. The script remains canonical so the result can be
recreated and checked.

## One-command bootstrap

The two canonical bootstrap artifacts are:

```text
structure.sh
structure.ps1
```

Either script creates or refreshes the repo-local helper environment,
including:

```text
.portable_bashrc
.portable_profile.ps1
setup_shell_repo_env.sh
setup_shell_repo_env.ps1
tools/pytouch.py
tools/pytree.py
```

No script edits the user's real shell profile or permanently changes the
machine environment.

### Bash

```bash
bash structure.sh
./setup_shell_repo_env.sh
```

### PowerShell

```powershell
.\structure.ps1
.\setup_shell_repo_env.ps1
```

## First experiment

```bash
python scripts/run_first_experiment.py
```

This:

1. loads the corpus;
2. normalizes and classifies tokens;
3. writes canonical run data;
4. creates the logarithmic boundary visualization;
5. trains small word and character n-gram models;
6. writes sample generations and summary statistics.

## Tests

```bash
python -m pytest
```

## Design principle

> Portable developer ergonomics, zero persistent machine configuration.

And one pacing principle:

> No feature is blocked solely because every line has not yet been studied.

## Corpus retrieval and project recovery — 2026-10-18

Recovery session start: `2026-10-18T13:17:23-04:00`
Retrieval confirmed by: `2026-10-18T13:56:08-04:00`
Timezone: America/New_York (EDT, UTC−04:00)

The corpus was retrieved during this interval. The exact download
completion timestamp was not recorded.

The elapsed recovery window was 38 minutes, 45 seconds, including
environment setup, dependency installation, download, and initial
inspection—not just download time.

The resulting UTF-8 file, `war_and_peace_ru_fr_wikisource.txt`, contains
5,154,939 bytes. Initial inspection confirmed Russian prose with
embedded French in the opening of Volume 1. Full-corpus completeness
has not yet been verified.

The historical `build_status.json` failure record predates this
successful retrieval and is not updated automatically by the builder.
