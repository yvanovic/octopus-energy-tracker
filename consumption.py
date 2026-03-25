import pandas as pd

from data import consumption_data

# Octopus Energy tariff rates (pence per kWh) by hour
TARIFF_RATES = {
    "shoulder": {
        "hours": set(range(4, 7)) | set(range(13, 16)) | set(range(22, 24)),
        "rate": 14.13,
    },
    "off_peak_night": {"hours": set(range(0, 4)), "rate": 28.82},
    "mid_peak": {"hours": set(range(7, 13)), "rate": 28.82},
    "off_peak_evening": {"hours": set(range(19, 22)), "rate": 28.82},
    "peak_evening": {"hours": set(range(16, 19)), "rate": 43.22},
}

FLAT_RATE = 28.43  # Old flat rate comparison


def get_rate_for_hour(hour: int) -> float:
    """Return the unit rate (pence per kWh) for a given hour."""
    for _, data in TARIFF_RATES.items():
        if hour in data["hours"]:
            return data["rate"]
    return FLAT_RATE


def process_consumption_data(raw_data: list) -> pd.DataFrame:
    """
    Process raw consumption data and calculate costs.

    Returns a DataFrame with hourly consumption, rates, and costs.
    """
    if not raw_data:
        raise ValueError("No consumption data available")

    df = pd.json_normalize(raw_data)

    # Parse timestamps and extract date/hour
    df["datetime"] = pd.to_datetime(df["interval_start"])
    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour
    df["time"] = df["datetime"].dt.strftime("%H:%M")

    # Calculate rate based on tariff
    df["rate_pence_per_kwh"] = df["hour"].apply(get_rate_for_hour)

    # Calculate costs (consumption is in kWh, rates are in pence)
    df["cost_new"] = (df["consumption"] * df["rate_pence_per_kwh"]) / 100
    df["cost_flat"] = (df["consumption"] * FLAT_RATE) / 100
    df["savings"] = df["cost_flat"] - df["cost_new"]

    # Add period labels
    def get_period(hour):
        if 4 <= hour < 7 or 13 <= hour < 16 or 22 <= hour < 24:
            return "Shoulder (14.13p)"
        elif 16 <= hour < 19:
            return "Peak (43.22p)"
        elif 7 <= hour < 13:
            return "Mid-peak (28.82p)"
        else:
            return "Off-peak (28.82p)"

    df["period"] = df["hour"].apply(get_period)

    # Clean up
    df = df.drop(["interval_end", "interval_start", "datetime"], axis=1)

    return df


daily_data = process_consumption_data(consumption_data)
