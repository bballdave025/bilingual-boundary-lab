$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:BBL_REPO_ROOT = $RepoRoot
$env:PYTHONPATH = if ($env:PYTHONPATH) {
    "$RepoRoot/src$([IO.Path]::PathSeparator)$env:PYTHONPATH"
} else {
    "$RepoRoot/src"
}
$env:PATH = "$RepoRoot/tools$([IO.Path]::PathSeparator)$env:PATH"
Set-Location $RepoRoot

function pytouch {
    python "$env:BBL_REPO_ROOT/tools/pytouch.py" @args
}
function pytree {
    python "$env:BBL_REPO_ROOT/tools/pytree.py" @args
}
function bbltest {
    python -m pytest @args
}
function bblbuild {
    python scripts/build_war_and_peace_corpus.py @args
}
function bblrun {
    python scripts/run_first_experiment.py @args
}

function prompt {
    "(bbl) $($executionContext.SessionState.Path.CurrentLocation)> "
}
