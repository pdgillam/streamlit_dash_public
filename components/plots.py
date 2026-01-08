import typing as t

import pandas as pd
import plotly.express as px
import altair as alt


def _empty_plotly_fig():
    """Return an empty plotly Figure placeholder."""
    return px.scatter(pd.DataFrame({"x": [], "y": []}), x="x", y="y")


def line_chart_plotly(df: pd.DataFrame) -> "plotly.graph_objs._figure.Figure":
    """Create a time series line chart of `value` over `timestamp`.

    If `category` exists, lines are colored by category.
    """
    if df is None or df.shape[0] == 0:
        return _empty_plotly_fig()

    df = df.copy()
    if "timestamp" not in df.columns or "value" not in df.columns:
        return _empty_plotly_fig()

    # Ensure timestamp is datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    color = "category" if "category" in df.columns else None
    fig = px.line(df.sort_values("timestamp"), x="timestamp", y="value", color=color, markers=True)
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    return fig


def bar_chart_plotly(df: pd.DataFrame, agg: str = "mean") -> "plotly.graph_objs._figure.Figure":
    """Create a bar chart aggregated by `category` showing aggregated `value`.

    agg: one of 'mean'|'sum'|'count'
    """
    if df is None or df.shape[0] == 0:
        return _empty_plotly_fig()

    if "category" not in df.columns:
        return _empty_plotly_fig()

    if agg == "sum":
        agg_df = df.groupby("category")["value"].sum().reset_index()
        y = "value"
    elif agg == "count":
        agg_df = df.groupby("category").size().reset_index(name="value")
        y = "value"
    else:
        agg_df = df.groupby("category")["value"].mean().reset_index()
        y = "value"

    fig = px.bar(agg_df, x="category", y=y, color="category", text=y)
    fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
    return fig


def scatter_altair(df: pd.DataFrame) -> alt.Chart:
    """Return an Altair scatter plot of `value` vs `score`, colored by category if present."""
    if df is None or df.shape[0] == 0:
        # return an empty Altair Chart
        empty = pd.DataFrame({"value": [], "score": []})
        return alt.Chart(empty).mark_circle().encode(x="value", y="score")

    df = df.copy()
    if "value" not in df.columns or "score" not in df.columns:
        empty = pd.DataFrame({"value": [], "score": []})
        return alt.Chart(empty).mark_circle().encode(x="value", y="score")

    enc = alt.Chart(df).mark_circle(size=60).encode(x="value:Q", y="score:Q")
    if "category" in df.columns:
        enc = enc.encode(color="category:N")
    enc = enc.properties(width=300, height=400)
    return enc

