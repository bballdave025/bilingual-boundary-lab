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
