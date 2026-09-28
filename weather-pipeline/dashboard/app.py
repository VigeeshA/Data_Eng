from pathlib import Path

import duckdb
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "weather.duckdb"

st.set_page_config(page_title="Weather Forecast", layout="wide")
st.title("Three-Day Weather Forecast")
st.caption("Daily summaries from Open-Meteo, transformed with dbt.")

if not DATABASE.exists():
    st.error("Database not found. Run the ingestion and dbt commands first.")
    st.stop()

with duckdb.connect(str(DATABASE), read_only=True) as con:
    df = con.execute(
        """
        select
            city,
            forecast_date,
            avg_temperature_c,
            min_temperature_c,
            max_temperature_c,
            total_precipitation_mm,
            avg_wind_speed_kmh
        from analytics_daily_weather
        order by city, forecast_date
        """
    ).df()

if df.empty:
    st.warning("No forecast data found. Run the pipeline again.")
    st.stop()

city = st.selectbox("Choose a city", sorted(df["city"].unique()))
city_df = df[df["city"] == city].copy()

st.subheader(f"Forecast for {city}")
st.line_chart(
    city_df.set_index("forecast_date")[
        ["avg_temperature_c", "min_temperature_c", "max_temperature_c"]
    ]
)

st.subheader("Daily details")
st.dataframe(city_df, use_container_width=True)
