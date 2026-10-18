$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
pwsh -NoProfile -NoExit -Command `
    ". '$RepoRoot/.portable_profile.ps1'"
