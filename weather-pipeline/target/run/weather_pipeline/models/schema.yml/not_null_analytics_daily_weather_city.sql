
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select city
from "weather"."main"."analytics_daily_weather"
where city is null



  
  
      
    ) dbt_internal_test