
    
    

select
    city_forecast_date as unique_field,
    count(*) as n_records

from "weather"."main"."analytics_daily_weather"
where city_forecast_date is not null
group by city_forecast_date
having count(*) > 1


