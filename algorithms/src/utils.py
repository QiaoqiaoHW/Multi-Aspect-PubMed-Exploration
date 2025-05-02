import datetime

def fetch_one_day_data(date, client, index_name, size=20):
    query = {"query": {"term": {"articleDate": {"value": date}}}}

    data = client.search(body=query, index=index_name, size=size, pretty=True)
    return data["hits"]["hits"]


def fetch_data(begin_date, end_date, client, index_name, size=20):
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    data = []
    while begin_date <= end_date:
        # print(begin_date)
        date_str = begin_date.strftime("%Y-%m-%d")
        one_day_data = fetch_one_day_data(
            date_str, client, index_name=index_name, size=size
        )
        data += one_day_data
        begin_date += datetime.timedelta(days=1)

    return data
    