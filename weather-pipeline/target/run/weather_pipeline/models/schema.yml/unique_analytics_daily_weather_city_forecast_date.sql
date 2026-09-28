
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    city_forecast_date as unique_field,
    count(*) as n_records

from "weather"."main"."analytics_daily_weather"
where city_forecast_date is not null
group by city_forecast_date
having count(*) > 1



  
  
      
    ) dbt_internal_test