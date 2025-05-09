import csv

from snowhouse.browser_connection import set_connection, close_connection
from queries.credits.wh_usage import WAREHOUSES_CREDITS


# Python SQL Functions for Snowflake

def get_warehouse_level_query( salesforce_id):

    warehouse_credits_query = WAREHOUSES_CREDITS.format(salesforce_id)
    print(warehouse_credits_query)
    return warehouse_credits_query


def fetch_results(warehouse_credits_query):
    warehouse_credits_list = []

    result = cursor.execute(warehouse_credits_query).fetchall()

    for row in result:
        warehouse_credits_list.append(row)

    return warehouse_credits_list


if __name__ == '__main__':
    cursor = set_connection("TECHNICAL_ACCOUNT_MANAGER", "SNOWHOUSE")

    salesforce_ids = ["0013100001fp9ovAAA", "0013100001fm0GiAAI"]
    # , ["0013100001gYxA7AAK", "0010Z00001tHHwLQAW", "0013100001dGcigAAC"]
    salesforce_names = ['SurveyMonkey', "Acxiom LLC" ]
    # ["Saks.com LLC""Asics Digital", "Basis Technologies", "Mobilityware Inc"]

    for i in range(len(salesforce_ids)):
        salesforce_id = salesforce_ids[i]
        salesforce_name = salesforce_names[i]

        warehouse_credits_query = get_warehouse_level_query( salesforce_id)

        warehouse_credits_list = fetch_results(warehouse_credits_query)

        with open(f'output/wh_{salesforce_name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            for row in warehouse_credits_list:
                output_row = ["" if item is None else item for item in row]
                writer.writerow(output_row)

    close_connection(cursor)
