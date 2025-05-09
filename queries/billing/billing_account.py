BILLING_ACCOUNT = """
select 
    DATE_TRUNC('MONTH', general_date::DATE) AS "MONTH",
    SNOWFLAKE_ACCOUNT_ID,
    SNOWFLAKE_ACCOUNT_NAME,
    CLOUD_PROVIDER_REGION,
    sum(compute_revenue) as "COMPUTE",
    sum(daily_storage_revenue) as "STORAGE",
    sum(total_compute_revenue) -  sum(compute_revenue)  as "OTHERS",
from finance.customer.snowflake_account_revenue_etm 
where salesforce_account_id = '{}'
and general_date >= '{}' and general_date <= '{}'
group by all
order by 1
"""