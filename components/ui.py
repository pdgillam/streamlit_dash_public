import typing as t

import pandas as pd

# Defer importing streamlit to runtime so unit tests can import this module
# without requiring streamlit to be installed. Provide a no-op fallback for
# the `cache_data` decorator when streamlit is not available.
try:
    import streamlit as st  # type: ignore
except Exception:
    class _STStub:
        @staticmethod
        def cache_data(func=None, **_):
            # Behaves as a decorator: if func provided, return it, otherwise
            # return an identity decorator.
            if func is None:
                def _decorator(f):
                    return f
                return _decorator
            return func

        @staticmethod
        def dataframe(_df):
            return None

        @staticmethod
        def write(*_a, **_k):
            return None

        @staticmethod
        def download_button(*_a, **_k):
            return None

        @staticmethod
        def caption(*_a, **_k):
            return None

    st = _STStub()


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to CSV bytes for download."""
    return df.to_csv(index=False).encode('utf-8')


def filter_df(
    df: pd.DataFrame,
    categories: t.Optional[t.Iterable[str]] = None,
    start_date: t.Optional[t.Union[str, pd.Timestamp]] = None,
    end_date: t.Optional[t.Union[str, pd.Timestamp]] = None,
    text_search: t.Optional[str] = None,
) -> pd.DataFrame:
    """Filter DataFrame by category, date range, and free-text search.

    Args:
        df: source DataFrame (expects a 'timestamp' column)
        categories: iterable of category values to include
        start_date/end_date: inclusive date range filters
        text_search: substring to search across row values (case-insensitive)

    Returns:
        Filtered DataFrame (a view/copy depending on pandas behavior)
    """
    out = df
    if categories:
        out = out[out['category'].isin(list(categories))]
    if start_date is not None:
        out = out[out['timestamp'] >= pd.to_datetime(start_date)]
    if end_date is not None:
        out = out[out['timestamp'] <= pd.to_datetime(end_date)]
    if text_search:
        needle = text_search.lower()
        mask = out.apply(lambda row: needle in str(row.values).lower(), axis=1)
        out = out[mask]
    return out


@st.cache_data
def load_data_cached(_loader_func, *args, **kwargs):
    """Cache wrapper for data loading functions. Accepts a callable that returns a DataFrame.

    Example:
        df = load_data_cached(generate_fake_data, n=1000, seed=1)
    """
    return _loader_func(*args, **kwargs)


def try_show_aggrid(df: pd.DataFrame, height: int = 400, **aggrid_kwargs) -> t.Optional[pd.DataFrame]:
    """If `st_aggrid` is installed, show an interactive grid with selection and return the selected rows.

    If `st_aggrid` is not installed, fall back to `st.dataframe` and return None.
    """
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder
        from st_aggrid.shared import GridUpdateMode
    except Exception:
        st.dataframe(df)
        return None

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode='single', use_checkbox=False)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        height=height,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        **aggrid_kwargs,
    )

    selected = grid_response.get('selected_rows', [])
    if selected:
        return pd.DataFrame(selected)
    return None
