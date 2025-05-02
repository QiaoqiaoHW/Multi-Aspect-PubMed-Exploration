import uvicorn
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from collections import Counter, defaultdict

from utils.connection import client
from utils.utilities import *
from utils.query_data import *
from utils.config import *

app = FastAPI()

# add middleware to allow cross origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

min_date,max_date = get_min_and_max_date(client,index_name_insights)
# min_date = "2019-01-01"
# max_date = "2020-04-30"
# print(min_date, max_date)


######
# nodesGraph part
######
@app.get("/nodes/mode/{mode}")
async def get_global_data_by_batch(mode: str = "topical", scroll_id: str = None):
    print(min_date,max_date)
    query = generate_nodes_query(min_date,max_date,dim_reduction_method,clustering_method,reference_text)
    if mode == "topical":
        if not scroll_id:
            batch_data = query_first_batch(client=client,index_name=index_name_insights,query=query,size=1000,scroll="10m")
        else:
            batch_data = query_batch_by_scroll_id(client,scroll_id)
        
        elements = batch_data["elements"]  
        element_groups = [{"id":"topical", "level":"topical", "elements":elements,
                           "start_date":min_date,"end_date":max_date}]

        return {"scroll_id":batch_data["scroll_id"], "scroll_size":batch_data["scroll_size"], "element_groups":element_groups}
    
    if mode=="temporal":
        group_key = "year"
        groups = []
        if not scroll_id:
            batch_data = query_first_batch(client=client,index_name=index_name_insights,query=query,size=1000,scroll="10m")
            groups = generate_groups(min_date,max_date,group_key)
        else:
            batch_data = query_batch_by_scroll_id(client,scroll_id)

        element_groups = sort_group_by_key(batch_data["elements"],group_key)
        element_groups.sort(key=lambda item:item["elements"][0]["data"]["articleDate"])

        if groups:
            for group in groups:
                for element_group in element_groups:
                    if group['id'] == element_group['id']:
                        group['elements'].extend(element_group['elements'])
                        break
            element_groups = groups

        return {"scroll_id":batch_data["scroll_id"], "scroll_size":batch_data["scroll_size"], 
                "element_groups":element_groups}

    return {"error":"check the mode"}


@app.post("/nodes/show")
async def get_selected_data_by_batch(scroll_id: str = None, start_date: str = Form(), end_date: str = Form()):
    group_key = calculate_group_key(start_date,end_date)
    groups = []
    if not scroll_id:
        query = generate_nodes_query(start_date,end_date,dim_reduction_method,clustering_method,reference_text)
        batch_data = query_first_batch(client=client,index_name=index_name_insights,query=query,size=1000,scroll="10m")
        groups = generate_groups(start_date,end_date,group_key)
    else:
        batch_data = query_batch_by_scroll_id(client,scroll_id)

    element_groups = sort_group_by_key(batch_data["elements"],group_key)
    element_groups.sort(key=lambda item:item["elements"][0]["data"]["articleDate"])
    if groups:
        for group in groups:
            for element_group in element_groups:
                if group['id'] == element_group['id']:
                    group['elements'].extend(element_group['elements'])
                    break
        element_groups = groups

    return {"scroll_id":batch_data["scroll_id"], "scroll_size":batch_data["scroll_size"], 
            "element_groups":element_groups}
    
######
# wordCloud part
######
@app.get("/wordcloud/mode/{mode}")
async def get_global_word_cloud(mode: str = "global", size: int = None):
    query = {"query": { "range": {"articleDate": {"gte": min_date, "lte": max_date}}}}
    data = client.search(
                body = query,
                index = index_name_words,
                size=10000,
                scroll = "10m",
                pretty = True)
    
    scroll_id = data["_scroll_id"]
    scroll_size = len(data["hits"]["hits"])
    if mode == "global":
        word_counter = Counter()
        while scroll_size>0:
            for item in data["hits"]["hits"]:
                counter = Counter(item["_source"]["words"])
                word_counter.update(counter)

            data = client.scroll(scroll_id=scroll_id, scroll="10m")
            scroll_id = data["_scroll_id"]
            scroll_size = len(data["hits"]["hits"])

        # word_counter = word_counter.most_common()[:size]
        word_counter = word_counter.most_common()
        if len(word_counter)>=size:
            word_counter = word_counter[:size]
        return {"wordData":[{"id":"global","level":"global","word_group":word_counter}]}


    if mode=="temporal":
        groups = defaultdict(Counter)
        while scroll_size>0:
            for item in data["hits"]["hits"]:
                articleDate = item["_source"]["articleDate"]
                year = datetime.strptime(articleDate, "%Y-%m-%d").year
                word_counter = Counter(item["_source"]["words"])
                groups[year].update(word_counter)

            data = client.scroll(scroll_id=scroll_id, scroll="10m")
            scroll_id = data["_scroll_id"]
            scroll_size = len(data["hits"]["hits"])

        word_groups = []
        for year, counter in groups.items():
            counter = counter.most_common()
            if len(counter)>=size:
                counter = counter[:size]
            group = {"id":year,"level":"year","word_group":counter}
            word_groups.append(group)

        return {"wordData":word_groups}
     

@app.post("/wordcloud/show")
async def get_selected_word_cloud(size: int = None, start_date: str = Form(), end_date: str = Form()):
    group_key = calculate_group_key(start_date,end_date)
    query = {"query": { "range": {"articleDate": {"gte": start_date, "lte": end_date}}}}
    data = client.search(
                body = query,
                index = index_name_words,
                size=10000,
                scroll = "10m",
                pretty = True)
    
    scroll_id = data["_scroll_id"]
    scroll_size = len(data["hits"]["hits"])

    groups = defaultdict(Counter)
    selected_counter = Counter()
    while scroll_size>0:
        for item in data["hits"]["hits"]:
            articleDate = item["_source"]["articleDate"]
            time_levels = get_year_month_quarter_and_week(articleDate)
            word_counter = Counter(item["_source"]["words"])
            groups[time_levels[group_key]].update(word_counter)
            selected_counter.update(word_counter)

        data = client.scroll(scroll_id=scroll_id, scroll="10m")
        scroll_id = data["_scroll_id"]
        scroll_size = len(data["hits"]["hits"])
    
    selected_counter = selected_counter.most_common()
    if len(selected_counter)>=size:
        selected_counter = selected_counter[:size]
    selectedWord = {"id":"selectedWord","level":"selectedWord","word_group":selected_counter}

    word_groups = []
    for key, counter in groups.items():
        counter = counter.most_common()
        if len(counter)>=size:
            counter = counter[:size]
        group = {"id":key,"level":group_key,"word_group":counter}
        word_groups.append(group)
    
    return {"wordData":word_groups,"selectedAllWord":selectedWord}

######
# filter part
######
@app.post("/filter/nodes")
async def filter_nodes(search_word: str = Form(), aspect: str = Form(),start_date: str = Form(), end_date: str = Form()):
    min_date,max_date = get_min_and_max_date(client,index_name_insights)
    # min_date = "2019-09-01"
    # max_date = "2020-04-30"
    min_date = "2019-01-01"
    max_date = "2021-12-31"
    if start_date!="global":
        min_date = start_date
        max_date = end_date

    kw = "should"
    if aspect=="title":
        match = [{"match": {"title": search_word}}]
    if aspect=="abstract":
        match = [{"match": {"abstract": search_word}}]
    if aspect=="title+abstract":
        match = [{"match": {"title": search_word}}, {"match": {"abstract": search_word}}]
    if aspect=="keywords":
        match = [{"nested": {"path": "keywords", "query": {"match": {"keywords.name": search_word}}}}]
    if aspect=="journal":
        match = [{"nested": {"path": "journalInformation", "query": {"match": {"journalInformation.journalTitle": search_word}}}}]        # match = [{"match": {"journalInformation.journalTitle": search_word}}]
    if aspect=="affiliations":
        match = [{"match": {"authors.affiliations.institute": search_word}}]
    if aspect=="authors":
        name_components = search_word.split(" ")
        if len(name_components)==1:
            kw = "should"
            lastName = name_components[-1].capitalize()
            firstName = lastName
        elif len(name_components)>=2:
            kw = "must"
            lastName = name_components[-1].capitalize()
            firstName = " ".join([comp.capitalize() for comp in name_components[:-1]])
        match = [{"nested": {"path": "authors", "query": {"match": {"authors.firstName": firstName}}}},
                 {"nested": {"path": "authors", "query": {"match": {"authors.lastName": lastName}}}}]

    query = {"_source": ["_id"],
            "query": {"bool": 
                        {"must": [
                            {"bool": {
                                kw: match }
                            },
                            {"range": {
                                "articleDate": {
                                "gte": min_date,
                                "lte": max_date
                                }}
                            }]}}
            }     
    print(query)       
    
    data = client.search(
                body = query,
                index = index_name_pubmed,
                size=10000,
                scroll = "10m",
                pretty = True)
    
    scroll_id = data["_scroll_id"]
    scroll_size = len(data["hits"]["hits"])

    searchIds = []
    while scroll_size > 0:
        for item in data["hits"]["hits"]:
            searchIds.append(item["_id"])
        data = client.scroll(scroll_id=scroll_id, scroll="10m")
        scroll_id = data["_scroll_id"]
        scroll_size = len(data["hits"]["hits"])

    return {"searchIds":searchIds}


@app.post("/filter/wordcloud")
async def filter_wordcloud(search_word: str = Form(), aspect: str = Form(), idsGroup: str=Form(),size: int = None):
    ids = idsGroup.split(",")

    query = {"query": {"terms": {"_id": ids}}}
    data = client.search(
                body = query,
                index = index_name_words,
                size=10000,
                scroll = "10m",
                pretty = True)
    
    scroll_id = data["_scroll_id"]
    scroll_size = len(data["hits"]["hits"])

    filter_counter = Counter()
    while scroll_size>0:
        for item in data["hits"]["hits"]:
            word_counter = Counter(item["_source"]["words"])
            filter_counter.update(word_counter)

        data = client.scroll(scroll_id=scroll_id, scroll="10m")
        scroll_id = data["_scroll_id"]
        scroll_size = len(data["hits"]["hits"])

    if aspect in ["title","abstract","title+abstract"]:
        del filter_counter[search_word]

    filter_counter = filter_counter.most_common()
    if len(filter_counter)>=size:
        filter_counter = filter_counter[:size]
    elif len(filter_counter)==0:
        filter_counter = [("null",1)]

    filteredWord = {"id":"selectedWord","level":"selectedWord","word_group":filter_counter}
    return {"selectedAllWord":filteredWord}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True, debug=True)

