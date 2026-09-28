import json
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
DATABASE = ROOT / "weather.duckdb"

CITIES = {
    "London": {"latitude": 51.5072, "longitude": -0.1276},
    "New York": {"latitude": 40.7128, "longitude": -74.0060},
    "Tokyo": {"latitude": 35.6762, "longitude": 139.6503},
}


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fetched_at = datetime.now(timezone.utc).isoformat()
    records = []

    for city, location in CITIES.items():
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                **location,
                "hourly": (
                    "temperature_2m,"
                    "precipitation,"
                    "wind_speed_10m"
                ),
                "forecast_days": 3,
                "timezone": "UTC",
            },
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()

        # Save the original API response as raw data.
        safe_city = city.lower().replace(" ", "_")
        filename = f"{safe_city}_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.json"
        (RAW_DIR / filename).write_text(
            json.dumps(
                {
                    "city": city,
                    "fetched_at": fetched_at,
                    "response": payload,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        hourly = payload["hourly"]

        for i, forecast_time in enumerate(hourly["time"]):
            records.append(
                {
                    "city": city,
                    "fetched_at": fetched_at,
                    "forecast_time": forecast_time,
                    "temperature_c": hourly["temperature_2m"][i],
                    "precipitation_mm": hourly["precipitation"][i],
                    "wind_speed_kmh": hourly["wind_speed_10m"][i],
                }
            )

    df = pd.DataFrame(records)
    if df.empty:
        raise RuntimeError("The API returned no weather records.")

    # Store the current batch in a DuckDB raw table.
    with duckdb.connect(str(DATABASE)) as con:
        con.register("weather_dataframe", df)
        con.execute(
            "CREATE OR REPLACE TABLE raw_weather AS "
            "SELECT * FROM weather_dataframe"
        )

    print(f"Loaded {len(df)} hourly forecast rows into {DATABASE}")


if __name__ == "__main__":
    main()
