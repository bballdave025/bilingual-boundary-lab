from bbl.ngram import NGramModel


def test_zero_context_model() -> None:
    model = NGramModel[str](0).fit(list("aab"))
    assert model.distribution() == {"a": 2, "b": 1}


def test_one_context_model() -> None:
    model = NGramModel[str](1).fit(list("ababa"))
    assert model.distribution(["a"]) == {"b": 2}
    assert model.distribution(["b"]) == {"a": 2}


def test_seeded_generation_is_reproducible() -> None:
    model = NGramModel[str](1).fit(list("ababa"))
    first = model.generate(10, seed=["a"], random_seed=7)
    second = model.generate(10, seed=["a"], random_seed=7)
    assert first == second
