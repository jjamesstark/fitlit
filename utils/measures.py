import pandas as pd

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
