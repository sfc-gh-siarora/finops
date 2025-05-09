WAREHOUSES_CREDITS = """
      select
            YEAR(USAGE_DATE::DATE) || '-Q'  || QUARTER(USAGE_DATE::DATE) AS PERIOD
            ,DATE_TRUNC('month', USAGE_DATE::DATE) as MONTH
             ,map.salesforce_account_name
            ,m.SNOWFLAKE_ACCOUNT_ID  as ACCOUNT_ID
            ,WAREHOUSE_ID as "ENTITY_ID"
            ,WAREHOUSE_NAME as "ENTITY_NAME"
            ,ROUND(SUM(CREDITS),2) as CREDITS_XP
        from FINANCE.CUSTOMER.WAREHOUSE_COMPUTE m
         left join finance.customer.salesforce_snowflake_mapping map
            on m.snowflake_account_id = map.snowflake_account_id
         AND m.snowflake_deployment = map.snowflake_deployment
    WHERE true and
    map.salesforce_account_id = '{}'
    AND m.USAGE_DATE::DATE between '2023-01-01' AND DATEADD(day, -1, DATE_TRUNC('quarter', CURRENT_DATE()))
    AND m.WAREHOUSE_ID NOT IN (0,-2)
    and m.WAREHOUSE_NAME not like 'COMPUTE_SERVICE_WH_%'
    AND m.CREDITS > 0
    GROUP BY ALL 
"""
