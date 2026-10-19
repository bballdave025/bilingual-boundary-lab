# Preserve existing scaffold files by default; $false restores templates.
$do_very_safe_structure = $true

function Write-Scaffold {
    param([string]$Path, [string]$Value)
    if ($do_very_safe_structure -and (Test-Path -LiteralPath $Path)) {
        Write-Host "Preserving $Path"
        return
    }
    $encoding = New-Object System.Text.UTF8Encoding($false)
    $lfValue = $Value.Replace("`r`n", "`n").TrimEnd("`r", "`n") + "`n"
    [IO.File]::WriteAllText((Join-Path (Get-Location).Path $Path), $lfValue, $encoding)
}

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

$Directories = @(
    "data/raw",
    "data/processed",
    "docs",
    "experiments",
    "notebooks",
    "outputs/figures",
    "scripts",
    "src/bbl",
    "tests",
    "tools"
)

foreach ($Directory in $Directories) {
    New-Item -ItemType Directory -Force -Path $Directory | Out-Null
}

$Pytouch = @'
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    arguments = parser.parse_args()

    for path in arguments.paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)


if __name__ == "__main__":
    main()
'@

$Pytree = @'
from __future__ import annotations

import argparse
import fnmatch
from pathlib import Path

DEFAULT_EXCLUDES = (
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
)


def excluded(path: Path, patterns: list[str]) -> bool:
    return any(
        fnmatch.fnmatch(path.name, pattern)
        or fnmatch.fnmatch(path.as_posix(), pattern)
        for pattern in patterns
    )


def render(
    directory: Path,
    prefix: str,
    patterns: list[str],
) -> None:
    entries = sorted(
        (
            path
            for path in directory.iterdir()
            if not excluded(path, patterns)
        ),
        key=lambda path: (not path.is_dir(), path.name.lower()),
    )

    for index, path in enumerate(entries):
        last = index == len(entries) - 1
        branch = "└── " if last else "├── "
        print(f"{prefix}{branch}{path.name}")
        if path.is_dir():
            render(
                path,
                prefix + ("    " if last else "│   "),
                patterns,
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Bash-style wildcard; repeat as needed.",
    )
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    print(root.name)
    render(
        root,
        "",
        [*DEFAULT_EXCLUDES, *arguments.exclude],
    )


if __name__ == "__main__":
    main()
'@

$BashProfile = @'
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export BBL_REPO_ROOT="$repo_root"
export PYTHONPATH="$repo_root/src${PYTHONPATH:+:$PYTHONPATH}"
export PATH="$repo_root/tools:$PATH"
cd "$repo_root"

alias pytouch='python "$BBL_REPO_ROOT/tools/pytouch.py"'
alias pytree='python "$BBL_REPO_ROOT/tools/pytree.py"'
alias bbltest='python -m pytest'
alias bblbuild='python scripts/build_war_and_peace_corpus.py'
alias bblrun='python scripts/run_first_experiment.py'

PS1="(bbl) ${PS1:-\\u@\\h:\\w\\$ }"
'@

$PowerShellProfile = @'
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
'@

$BashLauncher = @'
#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash --noprofile --rcfile "$repo_root/.portable_bashrc" -i
'@

$PowerShellLauncher = @'
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
pwsh -NoProfile -NoExit -Command `
    ". '$RepoRoot/.portable_profile.ps1'"
'@

Write-Scaffold -Path "tools/pytouch.py" -Value $Pytouch
Write-Scaffold -Path "tools/pytree.py" -Value $Pytree
Write-Scaffold -Path ".portable_bashrc" -Value $BashProfile
Write-Scaffold -Path ".portable_profile.ps1" `
    -Value $PowerShellProfile
Write-Scaffold -Path "setup_shell_repo_env.sh" `
    -Value $BashLauncher
Write-Scaffold -Path "setup_shell_repo_env.ps1" `
    -Value $PowerShellLauncher

Write-Host "BBL repo-local helper environment refreshed."
