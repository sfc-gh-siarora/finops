DEPLOYMENT_REGIONS = """                 
with deployment_credits as(
    select
                m.SNOWFLAKE_DEPLOYMENT  as SNOWFLAKE_DEPLOYMENT
                ,ROUND(SUM(CREDITS),2) as CREDITS_XP
            from FINANCE.CUSTOMER.WAREHOUSE_COMPUTE m
             left join finance.customer.salesforce_snowflake_mapping map
                on m.snowflake_account_id = map.snowflake_account_id
             AND m.snowflake_deployment = map.snowflake_deployment
        WHERE 
        map.salesforce_account_id = '{}'
        AND m.USAGE_DATE::DATE between '2023-01-01' AND DATEADD(day, -1, DATE_TRUNC('quarter', CURRENT_DATE()))
        AND m.WAREHOUSE_ID NOT IN (0,-2)
        and m.WAREHOUSE_NAME not like 'COMPUTE_SERVICE_WH_%'
        AND m.CREDITS > 0
        GROUP BY ALL 
        HAVING CREDITS_XP > 1000
    )
select SNOWFLAKE_DEPLOYMENT from deployment_credits    
"""

