# Add script-switch prefix zoom and document Experiment 00

The full War and Peace script-run overview compresses individual runs.
Add `--num-language-changes N` to plot the first N switches (N+1 complete
runs), preserving overview dimensions and vertical scale. A request beyond
the available switches warns and uses all runs; negative requests error.
Prefix PNGs have distinct filenames and the x-axis identifies script-class
changes, including Numeric/Other transitions rather than language inference.

Includes 100/250/500/1000-change figures and Dave's annotated explorations,
README usage, virtual-environment/patch ignore rules, and Experiment 00
observations covering tokenization, mixed scripts, seeded generation,
rounded logarithmic bins, and translation round-trip overlap limitations.
Both scaffold scripts now preserve existing files by default while creating
missing templates. Add continuation documentation with reusable PCDP/context
header/body templates, a bbl lab-notebook checkpoint from Project Selection
Summary, and a README-linked TESTME checklist.

## Validation

- Windows: all 19 Python tests passed; full experiment regenerated 6,370 runs.
- User inspected prefix figures; full overview regenerated with updated label.
- Bash safe mode: isolated preservation and repeat-run checks passed.
- PowerShell scaffold preservation: isolated Windows check PASSED on
  2026-10-19; existing sentinel preserved, missing files created, all six
  hashes unchanged on repeat. Procedure retained in TESTME.

## Limits and follow-up

Script classes are not language labels; run lengths count normalized tokens.
Normalization still strips punctuation/combining marks. Corpus completeness
and source passages behind highlighted patterns are not yet verified.
Follow-ups: longer generated-text comparison, then general-text generation
with a guiding notebook. No generation-model redesign in this PR.
