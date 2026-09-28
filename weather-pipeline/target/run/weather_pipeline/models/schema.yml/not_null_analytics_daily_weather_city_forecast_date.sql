
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select city_forecast_date
from "weather"."main"."analytics_daily_weather"
where city_forecast_date is null



  
  
      
    ) dbt_internal_test