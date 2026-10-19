*BEGIN: Context Document Header*

# CONTEXT DOCUMENT — Continuation

## Project

**Name:** bbl

**Description:** Bilingual Boundary Lab visualizes maximal token-script
runs in the Russian/French text of War and Peace and explores word/character
n-gram generation. It supports a portfolio and mentoring collaborations.

## Continuation Metadata

**Prepared at:** 1792412198_2026-10-19T08:16:38-0400

America/New_York (Boston time); timestamp generated in the assistant runtime.

**Continued from chat:** Project Selection Summary

**Also involving:**
- Fort Point NLP portfolio sprint and mentoring
- Statistical language models and translation round-trip observations

## Author / Source

**User (GitHub):** @bballdave025

## Intent for This Context

Finish the prefix-zoom PR without losing validation limits or pending work,
then compare a longer generated sample with observed corpus structure.

## Usage Instructions

Treat this as the recorded checkpoint; verify newer repository state before
editing. Continue with minimal re-derivation and keep implementation bounded.

*ENDOF: Context Document Header*

## Current State and Git

User works in PowerShell at `C:\David\my_repos_dwb\bilingual-boundary-lab`.
Venv `.venv_bbl`, Python 3.10.11, parent Python from Miniconda; invoking
`python` after activation resolves to the venv. `(base)` can remain visible.

Branch: `zoom-on-first-n-changes`. User committed `ab641db` (zoom code,
initial observations, tests, .gitignore, four zoom PNGs and five annotated
images under img/fun). No remote push, PR creation, or merge is confirmed.
Historical baseline commit is `de4e8e7`.

An initial follow-up patch failed because its observation-file context did
not exactly match. User supplied three current files. The rebuilt
`bbl-followup-safe-structure-context-readme-v2.patch` applied successfully.
Do NOT reapply old/cumulative patches. That v2 change includes structure
safety flags, expanded observations, and the context README/templates.
These follow-up changes have not yet been confirmed committed or pushed.

This closeout adds TESTME, README links, this LN, and a consolidated PR draft.
It is delivered as another incremental patch, not applied to the user's
Windows checkout automatically. GitHub connector writes previously failed
403 Resource not accessible by integration. User pushes using local SSH.

## Architecture and Data Flow

- `scripts/build_war_and_peace_corpus.py`: Wikisource parsed HTML to UTF-8
  corpus via Requests/Beautiful Soup; does not update build_status.json.
- `src/bbl/normalization.py`: NFKD; removes marks, retains letters/digits,
  maps punctuation to separators. Changes й to и, ё to е, removes accents.
- `src/bbl/runs.py`: classify normalized tokens, group adjacent equal classes.
  Codes Numeric=0, Cyrillic=1, Latin=2, Other=3. Run length counts TOKENS.
- `src/bbl/anomalies.py`: original whitespace tokens; flags multiple LETTER
  scripts, retaining punctuation in examples but ignoring it for detection.
- `src/bbl/visualization.py`: one run per column, symmetric rounded-log
  radius. Symmetry is constructed; horizontal arrangements are observed.
- `scripts/run_first_experiment.py`: full-corpus stats, overview/prefix plot,
  and already-existing short word/character generated samples in summary.
- `src/bbl/ngram.py`: context-count model with random weighted sampling;
  currently unseen full context falls back to global token frequencies
  (not a fully trained hierarchy of shorter-context backoff models).

## Corpus and Recorded Results

Recovered 2026-10-18 during 13:17:23–13:56:08 EDT (38m45s recovery/setup
window, not download duration). 5,154,939 bytes, 2,895,061 decoded characters,
450,660 normalized tokens, 2,746,016 normalized characters. Opening inspected;
full-corpus completeness is NOT verified. Builder headings remain present.

6,370 runs: Cyrillic 3,122; Latin 2,094; Numeric 806; Other 348.
359 mixed-script token occurrences; first 50 shown. Not punctuation count,
not necessarily unique spellings. Longest Latin run 599 tokens; four map
to radius 3. Dave correctly calls 599 order 10^3 using geometric boundaries.
Script is a proxy, not proof of French/Russian/German language identity.

## Zoom and Generation Semantics

`python scripts/run_first_experiment.py --num-language-changes 1000`
plots 1,001 whole runs. Exceeding available switches warns and plots all;
negative values error, zero keeps first run. Separate PNGs for 100/250/500/
1000; common figure size and full-corpus radius limit. No argument refreshes
the overview and still regenerates the same short samples.

Word contexts n=0,1,2,3 generate 100 tokens, starting with corpus `words[:n]`,
random seed 1729+n. Character contexts n=0,1,2,3,5 generate 500 characters,
starting with `characters[:n]`, random seed 2718+n. n=0 has empty prefix.
These are reproducible opening-conditioned demonstrations, not representative
sampling evidence. They include source-heading artifacts.

$$
P \left( w_t \mid w_{\lt t} \right) \approx P \left( w_t \mid w_{t-k}, \ldots, w_{t-1} \right)
$$.

Code n counts preceding context tokens; conventional n-gram order is n+1.
An n-gram model IS a statistical language model, not a neural language model.

## Validation and Explicit Remaining Test

User verified on Windows 2026-10-19: v2 patch check/apply successful;
`git diff --check` clean; 19 Python tests passed in 0.79s. Overview ran
twice and wrote 6,370 runs. No further repeat runs needed without changes.
Bash safe mode preservation/repeat checks passed in assistant environment.

PowerShell scaffold preservation PASSED on Windows, 2026-10-19: Dave
supplied actual output showing sentinel preservation, missing file creation,
and unchanged hashes for all six files on a second run. Python suite does
not test this. Procedure retained in TESTME; PowerShell version not captured.
Do not claim executed validation from code review alone. False/overwrite
mode is outside that check. Both structure scripts default safe=true;
create missing files, preserve existing ones. No numbered experiment dirs.

## Observations and Mentoring

Detailed findings and Dave's penguin/typewriter analogy live in
`docs/observation_docs/Experiment_00_Observations.md`. Generated word_n0 was
incoherent but user-reported translation supplied a fluent narrative;
back-translation exposed rewriting. Unicode-word ROUGE F1: R1 .253659,
R2 .009852, RL .156098; no stemming. Surface overlap is not semantic fidelity.

Dave enjoys the visualization and marked patterns in img/fun; musical
annotation identified by Dave as Russian national anthem. Inspect source
passages before explaining small interrupting runs or claiming languages.
Tests for learners should explain inputs/expectations/failures in strings,
not just display more pytest verbosity. Preserve hyphen/punctuation behavior
for this baseline; better normalization is deferred.

## Documentation Conventions

`docs/context_documents/README.md` derives from dwb-ip-notes template
`auxiliaries/template_ctx_doc_README.md`; keep PCDP/header/body templates.
Project marker bbl; exact originating chat Project Selection Summary.
User explicitly triggered creation with CTX, CTX, Context on 2026-10-19.

## Immediate Next Steps

1. Apply the new closeout patch after v2, inspect git status/diff.
2. PowerShell safety check is complete; do not rerun without a new reason.
3. Review overview label; stage intended docs/scripts/overview; commit/push.
4. Open PR with consolidated draft in docs/dev_notes; verify file list;
   merge only after review, then update local main.
5. Source-passage inspection is deferred analysis, not a prerequisite for
   this bounded PR. Do not claim it completed.

## Two Follow-up Subjects

1. One longer generation from one chosen n-gram model, compared with actual
   text of matched token length under identical preprocessing/visual scale;
   switch count is measured, not forced. Later examine multiple seeds and
   starting contexts before generalizing.
2. General-text generator with configurable maximum context order and a
   guiding Jupyter notebook. Optional thin CLI; notebook is learner interface.

## Wider Portfolio Context (Deferred)

Original four-hour plan: BBL, FLAN-T5/LoRA historical reproduction and modern
seq2seq repair, JabberVec SVD, English Gorf, Job Frequency consolidation.
Those other projects have not been implemented in this BBL work. Keep
current closeout from expanding into that wider sprint.

## Closeout update — 2026-10-19, after supplied safety output

Latest Windows Python check: 19 passed in 0.64s. PowerShell safe-mode
check explicitly printed PASS. No execution-policy change was requested;
Dave's existing policy was Bypass. False/overwrite mode remains untested.
The overview was inspected and accepted by Dave. README now strikes through
its old pending-validation sentence and records PASS. Remove only that
historical struck-through sentence on the NEXT branch.

## Next branch: agreed scope and working style

The NEXT branch/PR should cover BOTH:

1. A guiding Jupyter notebook presenting the current artifact and planned
   direction at portfolio quality.
2. A reusable generator accepting a general text file and maximum CONTEXT
   order. Code n=k remembers k prior tokens; conventional n-gram order=k+1.
   Discuss the public option name before implementing to avoid ambiguity.

Longer generated-versus-real comparison remains planned; discuss its placement
rather than assuming another separate PR number. Do not implement these
follow-ups before finishing and syncing the current branch.

Dave wants to discuss README portfolio presentation later today. A notebook
would make him happier, but he explicitly chooses to work through that
incompleteness (his ERP framing) and bring other projects to the level of a
concrete artifact before endlessly polishing BBL. Do not turn this into an
unrequested therapeutic exercise or perfection-driven expansion.

Next device: Termux on the bus. git apply works there; Python environment
must be inspected separately because Windows venvs are not portable. All
code/docs/images must be committed and pushed first. Patch transfer files
are intentionally ignored; context docs and PR note are tracked. Current
remote push, PR creation, and merge remain unconfirmed until actual output.

Closeout PR note: docs/dev_notes/PR_comment_for_PR1_2026-10-19.md.
PCDP: docs/context_documents/PCDP_bbl_2026-10-19_-_termux-continuation.md.
