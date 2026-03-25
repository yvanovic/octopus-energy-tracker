"" "Data fetching and processing for Octopus Energy consumption data." ""
import os
from datetime import datetime, timedelta

import requests

API_KEY = os.getenv("OCTOPUS_API_KEY")
MPAN = os.getenv("OCTOPUS_MPAN")
SERIAL_METER = os.getenv("OCTOPUS_SERIAL_METER")

if not all([API_KEY, MPAN, SERIAL_METER]):
    raise ValueError(
        "Missing Octopus credentials. Set OCTOPUS_API_KEY, OCTOPUS_MPAN, and OCTOPUS_SERIAL_METER"
    )

BASE_URL = f"https://api.octopus.energy/v1/electricity-meter-points/{MPAN}/meters/{SERIAL_METER}/consumption"


def fetch_consumption(period_from: str, period_to: str) -> list:
    """
    Fetch hourly consumption data from Octopus Energy API.

    Args:
        period_from: ISO format date string (e.g., "2025-08-01T00:00:00Z")
        period_to: ISO format date string (e.g., "2025-08-02T00:00:00Z")

    Returns:
        List of consumption records
    """
    params = {
        "period_from": period_from,
        "period_to": period_to,
        "page_size": 100,
        "order_by": "period",
        "group_by": "hour",
    }

    response = requests.get(BASE_URL, params=params, auth=(API_KEY, ""), timeout=10)
    # Check for HTTP errors and raise an exception if the request was unsuccessful
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])


def get_today_consumption() -> list:
    """Fetch consumption data for today."""
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    period_from = today.isoformat() + "T00:00:00Z"
    period_to = tomorrow.isoformat() + "T00:00:00Z"

    return fetch_consumption(period_from, period_to)


def get_last_week_consumption() -> list:
    """Fetch consumption data for the last 7 days (ending yesterday)."""
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)

    period_from = week_ago.isoformat() + "T00:00:00Z"
    period_to = today.isoformat() + "T00:00:00Z"

    return fetch_consumption(period_from, period_to)


def get_demo_consumption() -> list:
    """Return sample consumption data for testing."""
    today = datetime.now().date()
    demo_data = []
    for hour in range(24):
        # Simulate varying consumption throughout the day
        if 7 <= hour < 9:
            consumption = 1.2  # Morning peak
        elif 12 <= hour < 14:
            consumption = 0.6  # Midday lower
        elif 18 <= hour < 20:
            consumption = 1.5  # Evening peak
        else:
            consumption = 0.4  # Off-peak

        start = datetime.combine(today, datetime.min.time()).replace(hour=hour)
        end = start + timedelta(hours=1)

        demo_data.append(
            {
                "consumption": consumption,
                "interval_start": start.isoformat() + "Z",
                "interval_end": end.isoformat() + "Z",
            }
        )
    return demo_data


# Try to fetch real data, fall back to demo data if unavailable
try:
    consumption_data = get_last_week_consumption()
    if not consumption_data:
        print("⚠️  No consumption data available for last week. Using demo data.")
        consumption_data = get_demo_consumption()
except Exception as e:
    print(f"⚠️  Could not fetch consumption data: {e}")
    print("Using demo data for visualization.")
    consumption_data = get_demo_consumption()
