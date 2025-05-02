import spacy
from src.connection import local_client as client


index_name_words = 'frameintell_pubmed_words'
index_name_text = 'frameintell_pubmed'
reference_text = 'title'

def create_index(index_name):
    try:
        response = client.indices.create(index_name)
        print("Creating index:")
        print(response)
    except Exception as e:
        print(e)


def get_data(min_date, max_date, index_name, size = 10000, scroll = '1m'):
    query = {"query": {
                "range": {"articleDate": {"gte": min_date,"lte": max_date}}
                    },
            "_source": ["title","abstract","articleDate"]
            }
    data = client.search(
            body = query,
            index = index_name,
            size=size,
            scroll = scroll,
            pretty = True
        )
    return data


def get_words_and_bulk_to_index(data,reference_text):
    docs = []
    for item in data['hits']['hits']:
        text = item['_source'][reference_text]
        doc = nlp(text)

        words = [token.lemma_.lower() for token in doc if token.pos_ == 'NOUN' and not token.is_stop]

        item_index = {"index": {"_index": index_name_words, "_id": item["_id"]}}
        item_data = {"reference_text":reference_text,
                     'articleDate':item['_source']['articleDate'],
                     'words': words}
        docs.append(item_index)
        docs.append(item_data)

    resp = client.bulk(body=docs, index=index_name_words)
    return resp


model = 'en_core_sci_sm'
nlp = spacy.load(model)

# List of stop words to be added
stop_words = ['.', ':', ',', '(',')', '[',']','?', '\\','/', '+', '-','\"','\'','1','2',' ']
# Add stop words to nlp.vocab
for word in stop_words:
    nlp.vocab[word].is_stop = True

min_date = '2019-01-01'
max_date = '2021-12-31'

if __name__ == '__main__':
    create_index(index_name_words)

    data = get_data(min_date,max_date,index_name_text,size = 5000)
    scroll_size = len(data['hits']['hits'])
    scroll_id = data['_scroll_id']

    while scroll_size>0:
        print(scroll_size)
        resp = get_words_and_bulk_to_index(data,reference_text)

        data = client.scroll(scroll_id=scroll_id,scroll='1m')
        scroll_id = data['_scroll_id']
        scroll_size = len(data['hits']['hits'])
    
