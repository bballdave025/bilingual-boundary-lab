from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

_TOKEN_RE = re.compile(r"\S+")


@dataclass(frozen=True, slots=True)
class MixedScriptToken:
    token: str
    scripts: tuple[str, ...]


def _letter_scripts(token: str) -> set[str]:
    scripts: set[str] = set()

    for character in unicodedata.normalize("NFKD", token):
        if not character.isalpha():
            continue
        name = unicodedata.name(character, "")
        if "CYRILLIC" in name:
            scripts.add("CYRILLIC")
        elif "LATIN" in name:
            scripts.add("LATIN")
        else:
            scripts.add("OTHER")

    return scripts


def find_mixed_script_tokens(text: str) -> list[MixedScriptToken]:
    """Detect but never autocorrect mixed-script source tokens."""
    findings: list[MixedScriptToken] = []

    for match in _TOKEN_RE.finditer(text):
        token = match.group(0)
        scripts = _letter_scripts(token)
        if len(scripts) > 1:
            findings.append(
                MixedScriptToken(token, tuple(sorted(scripts)))
            )

    return findings
