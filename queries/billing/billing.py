BILLING = """
select
    DATE_TRUNC('MONTH', general_date::DATE) AS "MONTH",
    sum(compute_revenue) as "COMPUTE",
    sum(daily_storage_revenue) as "STORAGE",
    sum(total_product_revenue) -  sum(compute_revenue) - sum(daily_storage_revenue)  as "OTHERS",
from finance.customer.snowflake_account_revenue_etm
where salesforce_account_id = '{}'
and general_date >= '2024-01-01' and general_date < DATE_TRUNC('MONTH', CURRENT_DATE)
group by all
order by 1
"""