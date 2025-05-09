from diskcache import Cache

cache = Cache('./my_cache')


def fetch_results(cursor, query):
    output_list = []

    result = cursor.execute(query).fetchall()

    column_headers = [description[0] for description in cursor.description]

    output_list.append(column_headers)
    for row in result:
        output_row = ["" if item is None else item for item in row]
        output_list.append(output_row)

    return output_list


def fetch_results_list_of_queries(cursor, queries, flag=0):
    list = []

    flag = 0

    for query in queries:
        print(query)

        result = cursor.execute(query).fetchall()
        if flag == 0:
            column_headers = [description[0] for description in cursor.description]
            if flag == 1:
                column_headers.append("CREDITS")
            list.append(column_headers)
            flag = 1

        for row in result:
            list.append(row)

    return list
