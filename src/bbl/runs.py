from __future__ import annotations

import enum
import unicodedata
from dataclasses import dataclass
from itertools import groupby

from .normalization import normalized_tokens


class ScriptClass(enum.IntEnum):
    NUMERIC = 0
    CYRILLIC = 1
    LATIN = 2
    OTHER = 3


@dataclass(frozen=True, slots=True)
class Run:
    script: ScriptClass
    length: int

    def as_pair(self) -> list[int]:
        return [int(self.script), self.length]


def character_script(character: str) -> ScriptClass:
    if character.isdecimal():
        return ScriptClass.NUMERIC

    name = unicodedata.name(character, "")
    if "CYRILLIC" in name:
        return ScriptClass.CYRILLIC
    if "LATIN" in name:
        return ScriptClass.LATIN
    return ScriptClass.OTHER


def classify_token(token: str) -> ScriptClass:
    scripts = {
        character_script(character)
        for character in token
        if character.isalpha() or character.isdecimal()
    }

    if not scripts:
        return ScriptClass.OTHER
    if scripts == {ScriptClass.NUMERIC}:
        return ScriptClass.NUMERIC
    if scripts <= {ScriptClass.CYRILLIC}:
        return ScriptClass.CYRILLIC
    if scripts <= {ScriptClass.LATIN}:
        return ScriptClass.LATIN
    return ScriptClass.OTHER


def build_runs(text: str) -> list[Run]:
    classes = [classify_token(token) for token in normalized_tokens(text)]
    return [
        Run(script=script, length=sum(1 for _ in members))
        for script, members in groupby(classes)
    ]
