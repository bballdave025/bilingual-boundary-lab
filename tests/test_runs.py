from bbl.runs import ScriptClass, build_runs, classify_token


def test_token_classification() -> None:
    assert classify_token("война") is ScriptClass.CYRILLIC
    assert classify_token("paix") is ScriptClass.LATIN
    assert classify_token("1812") is ScriptClass.NUMERIC
    assert classify_token("великaя") is ScriptClass.OTHER


def test_maximal_runs() -> None:
    runs = build_runs("война мир paix 1812 снова")
    assert [run.as_pair() for run in runs] == [
        [1, 2],
        [2, 1],
        [0, 1],
        [1, 1],
    ]
