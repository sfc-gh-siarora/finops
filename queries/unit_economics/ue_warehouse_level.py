UNIT_ECONOMICS = """SELECT
    YEAR(CREATED_ON::DATE) || '-Q'  || QUARTER(CREATED_ON::DATE) AS PERIOD,
    DATE_TRUNC('MONTH', CREATED_ON::DATE) AS "MONTH",
    ACCOUNT_ID,
    '' as ACCOUNT_NAME
    , J.WAREHOUSE_ID
    , J.WAREHOUSE_NAME
    , COUNT_IF(dur_xp_executing > 0) AS XP_JOBS
    , SUM(dur_xp_executing) AS dur_xp_executing
    , ROUND(SUM(DUR_XP_EXECUTING) / 1000 / 60 /60,1) AS CPU_HOURS
    , AVG(XP_CURRENT_CONCURRENCY_LEVEL) as AVG_CONCURRENCY
    , SUM(TOTAL_DURATION) AS TOTAL_DURATION
    , SUM(stats:stats.producedRows) as producedRows
    , SUM(stats:stats.ioLocalTempWriteBytes)+SUM(stats:stats.ioRemoteTempWriteBytes) as BYTES_SPILLED
    , SUM(coalesce(stats:stats:ioRemoteFdnWriteBytes::number, 0)) as BYTES_WRITTEN
    , SUM(coalesce(stats:stats:ioLocalFdnReadBytes::double, 0)) + SUM(coalesce(stats:stats:ioRemoteFdnReadBytes::double, 0))::int as BYTES_SCANNED
    , count(distinct user_id) as nb_users
    , count(distinct  DATABASE_ID) as nb_DB
    , count(distinct SCHEMA_ID) as nb_SCHEMA
    , count(distinct SESSION_ID) as nb_SESSION
    , count(distinct WAREHOUSE_ID) as nb_WH
FROM  SNOWHOUSE_IMPORT.{}.JOB_ETL_V J
WHERE j.ACCOUNT_ID  in ( SELECT distinct snowflake_account_id FROM
                finance.customer.salesforce_snowflake_mapping map
                WHERE
                map.salesforce_account_id  = '{}'
                and snowflake_deployment = '{}' )
AND   J.CREATED_ON::DATE BETWEEN '2023-01-01' AND DATEADD(day, -1, DATE_TRUNC('quarter', CURRENT_DATE()))
--todo: make it automated if possible to last day of quarter 
AND   DUR_XP_EXECUTING > 0
and WAREHOUSE_NAME not like 'COMPUTE_SERVICE_WH_%'
and WAREHOUSE_ID not in(0,-2)
GROUP BY ALL
"""

