select
    city,
    cast(forecast_time as date) as forecast_date,
    round(avg(temperature_c), 1) as avg_temperature_c,
    round(min(temperature_c), 1) as min_temperature_c,
    round(max(temperature_c), 1) as max_temperature_c,
    round(sum(precipitation_mm), 1) as total_precipitation_mm,
    round(avg(wind_speed_kmh), 1) as avg_wind_speed_kmh,
    city || '_' || cast(cast(forecast_time as date) as varchar)
        as city_forecast_date
from {{ ref('stg_weather') }}
group by
    city,
    cast(forecast_time as date)
