
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select forecast_time
from "weather"."main"."stg_weather"
where forecast_time is null



  
  
      
    ) dbt_internal_test