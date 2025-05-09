import csv
import logging

from threading import Lock
import concurrent.futures
from queries.unit_economics.deployment_regions import DEPLOYMENT_REGIONS
from queries.unit_economics.ue import UNIT_ECONOMICS_Q
from snowhouse.browser_connection import set_connection, close_connection


# TODO fix bug for result combining data! Do not use now.

def get_deployment_zone_queries(cs, salesforce_id):
    regions_query = DEPLOYMENT_REGIONS.format(salesforce_id)
    print(regions_query)

    results = cursor.execute(regions_query).fetchall()
    print(results)

    queries = []

    for zone in results:
        unit_economics_query = UNIT_ECONOMICS_Q.format(zone[0], salesforce_id, zone[0])
        queries.append(unit_economics_query)
    return queries


def execute_query(cs, query):
    print(query)
    result = cs.execute(query).fetchall()

    return result


def fetch_results():
    unit_economics_list = []
    max_parallel_queries = 4

    lock = Lock()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_parallel_queries) as executor:
        future_to_query = {executor.submit(execute_query, cursor, query): query for query in queries}

        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                result = future.result()
                with lock:  # Acquire the lock before accessing the shared resource
                    before_append = len(unit_economics_list)
                    for row in result:
                        unit_economics_list.append(row)
                    after_append = len(unit_economics_list)
                    logging.info(f"Appended {len(result)} rows from query {query}. List size is now {after_append}.")

            except Exception as exc:
                print(f"Query {query} generated an exception: {exc}")

    return unit_economics_list


if __name__ == '__main__':
    cursor = set_connection("TECHNICAL_ACCOUNT_MANAGER", "SNOWHOUSE")

    salesforce_id = "001i000000dpQ4cAAE"
    queries = get_deployment_zone_queries(cursor, salesforce_id)

    unit_economics_list = fetch_results()

    with open('output_adobe.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        for row in unit_economics_list:
            formatted_row = ["" if item is None else item for item in row]
            writer.writerow(formatted_row)

    close_connection(cursor)
