import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(page_title="Weight Loss: Goal vs Actual")
st.title("Weight Loss: Goal vs Actual")

st.sidebar.header("Options")
granularity = st.sidebar.radio("View", ["Weekly", "Daily"], index=0)


def load_weight_series(
    csv_url: str,
    date_column: str,
    weight_column: float,
    series_name: str,
) -> pd.DataFrame:
    """Load a weight time series from a CSV and tag it with a series label.

    Args:
        csv_url: URL or path to the CSV file to load.
        date_column: Name of the column containing the timestamp/date.
        date_column: Name of the column containing the weight.
        series_name: Label to assign to this series (e.g. "goals", "actuals").

    Returns:
        A DataFrame with columns ['date', 'Weight', 'series'].
    """
    df = pd.read_csv(csv_url)
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.rename(columns={date_column: "date"})
    df = df.rename(columns={weight_column: "weight"})

    weight_df = df[["date", "weight"]].copy()
    weight_df["series"] = series_name
    return weight_df


weight_goal_config = st.secrets["config"]["weight_goals"]
goal_weights_df = load_weight_series(**weight_goal_config)

actual_weight_config = st.secrets["config"]["weight_actuals"]
actual_weights_df = load_weight_series(**actual_weight_config)

combined = pd.concat(
    [d for d in [goal_weights_df, actual_weights_df] if d is not None],
    ignore_index=True,
)
combined = combined.set_index("date")

# --- Resample by granularity ---
freq = "D" if granularity == "Daily" else "W"

resampled = (
    combined.groupby("series")
    .resample(freq)["weight"]
    .mean()
    .reset_index()
    .dropna(subset=["weight"])
)

# --- Chart ---
chart = (
    alt.Chart(resampled)
    .mark_line(point=True)
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("weight:Q", title="weight", scale=alt.Scale(domain=[170, 195])),
        color=alt.Color("series:N", title="Series"),
    )
)

st.altair_chart(chart, theme="streamlit", use_container_width=True)

with st.expander("View underlying data"):
    st.dataframe(resampled.sort_values(["series", "date"]))
