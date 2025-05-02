from .utilities import transform_item_to_element

def query_first_batch(client,index_name,query,size=10000,scroll='1m'):
    data = client.search(
        body = query,
        index = index_name,
        size=size,
        scroll = scroll,
        pretty = True
    )
    scroll_id = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])

    elements = []
    for item in data['hits']['hits']:
        element = transform_item_to_element(item)
        elements.append(element)

    return {'scroll_id':scroll_id, 'scroll_size':scroll_size, 'elements':elements}


def query_batch_by_scroll_id(client,scroll_id,scroll='1m'):
    data = client.scroll(
        scroll_id=scroll_id, 
        scroll=scroll
    )
    scroll_id = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])

    elements = []
    for item in data['hits']['hits']:
        element = transform_item_to_element(item)
        elements.append(element)

    return {'scroll_id':scroll_id, 'scroll_size':scroll_size, 'elements':elements}


def get_min_and_max_date(client,index_name):
    query = { "size": 0,
              "aggs": { 
                    "min_date": { "min": { "field": "articleDate" } }, 
                    "max_date": { "max": { "field": "articleDate" } } 
                    } 
            }
    data = client.search(
        body = query,
        index = index_name,
        # size=size,
        pretty = True
    )

    min_date = data['aggregations']['min_date']['value_as_string'].split('T')[0]
    max_date = data['aggregations']['max_date']['value_as_string'].split('T')[0]
    
    return min_date,max_date