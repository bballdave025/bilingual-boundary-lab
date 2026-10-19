# TESTME — BBL development checks

## Recorded status — 2026-10-19

- Windows: 19 Python tests passed in 0.64 seconds (user-provided output).
- Full-corpus experiment completed: 6,370 runs; overview regenerated.
- Bash: syntax and isolated repeat-run preservation checks passed in the
  assistant environment.
- PowerShell: isolated safe-mode check PASSED on Windows, 2026-10-19.
  Existing sentinel edits survived, missing files were created, and all six
  file hashes matched after the second run. Actual output was supplied by
  Dave in Project Selection Summary. Python tests do not cover this behavior.
  PowerShell version was not captured.

## Python regression suite

Run from the repository root with the project venv active:

```powershell
python -m pytest -o addopts="" -v
```

## PowerShell scaffold safety — isolated temporary copy

Run this block from the repository root. It never runs the structure
script against the live checkout. It leaves the temporary directory for
inspection. Stop on any error; do not mark this check passed merely
because the Python suite passed.

```powershell
$ErrorActionPreference = 'Stop'
$originalLocation = (Get-Location).Path
$testRoot = Join-Path ([IO.Path]::GetTempPath()) ('bbl-structure-test-' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $testRoot | Out-Null
Copy-Item .\structure.ps1 (Join-Path $testRoot 'structure.ps1')

try {
    Set-Location $testRoot
    New-Item -ItemType Directory -Path tools | Out-Null
    $sentinel = Join-Path $testRoot 'tools/pytouch.py'
    [IO.File]::WriteAllText($sentinel, "# existing learner edits: preserve me`n")
    $sentinelHash = (Get-FileHash $sentinel -Algorithm SHA256).Hash

    & .\structure.ps1
    if ((Get-FileHash $sentinel -Algorithm SHA256).Hash -ne $sentinelHash) {
        throw 'Safe mode overwrote existing learner edits.'
    }

    $expected = @(
        'tools/pytouch.py', 'tools/pytree.py',
        '.portable_bashrc', '.portable_profile.ps1',
        'setup_shell_repo_env.sh', 'setup_shell_repo_env.ps1'
    )
    $firstHashes = @{}
    foreach ($file in $expected) {
        if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
            throw "Missing scaffold file: $file"
        }
        $firstHashes[$file] = (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash
    }

    & .\structure.ps1
    foreach ($file in $expected) {
        if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash -ne $firstHashes[$file]) {
            throw "Second safe run changed $file"
        }
    }
    Write-Host 'PASS: existing edits preserved; missing files created; second run unchanged.'
} finally {
    Set-Location $originalLocation
    Write-Host "Inspection directory: $testRoot"
}
```

If script execution is blocked by local policy, record that as blocked,
not passed. Do not change machine-wide policy just for this check.
The explicit false/overwrite mode has not been tested by this block.

## Visual checks

- Overview and prefix detail use the same dimensions and vertical scale.
- 100 requested changes yield 101 complete script-class runs.
- Numeric and Other transitions count; this is not language identification.
- No-option invocation saves the overview; prefix invocations save distinct PNGs.
- Confirm the regenerated overview has the updated script-class x-axis label.

## Record the result

Add date/time, PowerShell version (`$PSVersionTable.PSVersion`), and actual
PASS/error output to the lab notebook after executing the isolated check.
Keep unfinished work explicitly marked pending.
