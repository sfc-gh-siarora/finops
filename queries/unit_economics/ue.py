UNIT_ECONOMICS_Q = """SELECT
    YEAR(CREATED_ON::DATE) || '-Q'  || QUARTER(CREATED_ON::DATE) AS PERIOD
    , count(distinct user_id) as nb_users
    , count(distinct  ACCOUNT_ID || DATABASE_NAME) as nb_DB
    , count(distinct ACCOUNT_ID || DATABASE_NAME || SCHEMA_NAME) as nb_SCHEMA
    , count(distinct ACCOUNT_ID || SESSION_ID) as nb_SESSION
    , count(distinct ACCOUNT_ID || WAREHOUSE_NAME) as nb_WH
FROM  SNOWHOUSE_IMPORT.{}.JOB_ETL_V J
WHERE 
j.ACCOUNT_ID  in ( SELECT distinct snowflake_account_id FROM
                finance.customer.salesforce_snowflake_mapping map
                WHERE
                map.salesforce_account_id  = '{}'
                and snowflake_deployment = '{}' )
AND   J.CREATED_ON::DATE BETWEEN '2023-01-01' AND DATEADD(day, -1, DATE_TRUNC('quarter', CURRENT_DATE()))
AND   DUR_XP_EXECUTING > 0
and WAREHOUSE_NAME not like 'COMPUTE_SERVICE_WH_%'
--todo: make it automated if possible to last day of quarter 
and WAREHOUSE_ID not in (0,-2)
GROUP BY ALL
"""
