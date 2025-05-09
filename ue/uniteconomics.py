import csv

from queries.unit_economics.deployment_regions import DEPLOYMENT_REGIONS
from queries.unit_economics.ue import UNIT_ECONOMICS_Q
from snowhouse.browser_connection import set_connection, close_connection


# Python SQL Functions for Snowflake

def get_deployment_zone_queries(cursor, salesforce_id):
    regions_query = DEPLOYMENT_REGIONS.format(salesforce_id)
    print(regions_query)

    results = cursor.execute(regions_query).fetchall()

    print(results)

    queries = []

    for zone in results:
        unit_economics_query = UNIT_ECONOMICS_Q.format(zone[0], salesforce_id, zone[0])
        queries.append(unit_economics_query)
    return queries


def fetch_results(queries):
    unit_economics_list = []

    for query in queries:
        print(query)

        result = cursor.execute(query).fetchall()
        for row in result:
            unit_economics_list.append(row)

    return unit_economics_list


if __name__ == '__main__':
    cursor = set_connection("TECHNICAL_ACCOUNT_MANAGER", "SNOWADHOC")

    salesforce_ids = ["0013100001nndgPAAQ"]
    salesforce_names = ["HCC Services Company, Inc."]
    # ["Saks.com LLC""Asics Digital", "Basis Technologies", "Mobilityware Inc"]

    for i in range(len(salesforce_ids)):
        salesforce_id = salesforce_ids[i]
        salesforce_name = salesforce_names[i]

        queries = get_deployment_zone_queries(cursor, salesforce_id)

        unit_economics_list = fetch_results(queries)

        with open(f'output/output_{salesforce_name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            for row in unit_economics_list:
                output_row = ["" if item is None else item for item in row]
                writer.writerow(output_row)

    close_connection(cursor)
