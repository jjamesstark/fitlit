import streamlit as st
import altair as alt
import pandas as pd

from utils.measures import load_weight_series

st.set_page_config(page_title="Weight Loss: Goal vs Actual")
st.title("Weight Loss: Goal vs Actual")

st.sidebar.header("Options")
granularity = st.sidebar.radio("View", ["Weekly", "Daily"], index=0)


weight_goal_config = st.secrets["config"]["weight_goals"]
goal_weights_df = load_weight_series(**weight_goal_config)

actual_weight_config = st.secrets["config"]["weight_actuals"]
actual_weights_df = load_weight_series(**actual_weight_config)

combined = pd.concat(
    [d for d in [goal_weights_df, actual_weights_df] if d is not None],
    ignore_index=True,
)
combined = combined.set_index("date")

freq = "D" if granularity == "Daily" else "W"

resampled = (
    combined.groupby("series")
    .resample(freq)["weight"]
    .mean()
    .reset_index()
    .dropna(subset=["weight"])
)

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
