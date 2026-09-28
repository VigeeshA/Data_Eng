
    

    create  table
      "weather"."main"."stg_weather__dbt_tmp"
  
    
    as (
      select
    city,
    cast(fetched_at as timestamptz) as fetched_at,
    cast(forecast_time as timestamptz) as forecast_time,
    cast(temperature_c as double) as temperature_c,
    cast(precipitation_mm as double) as precipitation_mm,
    cast(wind_speed_kmh as double) as wind_speed_kmh
from raw_weather
    );
    
  