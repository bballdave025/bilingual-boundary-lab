from bbl.normalization import normalized_tokens


def test_punctuation_is_a_separator() -> None:
    assert normalized_tokens("12:30 word—word") == [
        "12",
        "30",
        "word",
        "word",
    ]


def test_accents_are_decomposed() -> None:
    assert normalized_tokens("français déjà") == ["francais", "deja"]
