import builtins
import pandas as pd

from components.ui import df_to_csv_bytes, filter_df, try_show_aggrid


def test_df_to_csv_bytes():
    df = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
    b = df_to_csv_bytes(df)
    s = b.decode("utf-8")
    assert "x,y" in s
    assert "1,a" in s


def test_filter_df_combined_filters():
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2020-01-01", "2020-01-05", "2020-01-10"]),
        "category": ["A", "B", "C"],
        "text": ["foo", "bar", "baz"],
        "value": [10, 20, 30],
    })

    out = filter_df(
        df,
        categories=["B", "C"],
        start_date="2020-01-02",
        end_date="2020-01-10",
        text_search="ba",
    )

    # Expect the rows for categories B and C where the 'text' contains 'ba'
    assert len(out) == 2
    assert set(out["category"]) == {"B", "C"}


def test_try_show_aggrid_fallback(monkeypatch):
    # Force an ImportError when attempting to import st_aggrid so the fallback path runs
    orig_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith("st_aggrid"):
            raise ImportError("no st_aggrid")
        return orig_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    df = pd.DataFrame({"a": [1]})
    try:
        result = try_show_aggrid(df, height=10)
        assert result is None
    finally:
        # restore import to avoid side effects for other tests
        monkeypatch.setattr(builtins, "__import__", orig_import)

