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
