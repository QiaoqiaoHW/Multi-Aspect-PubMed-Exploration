from datetime import datetime, timedelta
from itertools import groupby

from .color_and_topic import colors_new_legend,topics_new_legend


def generate_nodes_query(min_date,max_date,dim_reduction_method='tsne',clustering_method='kmeans',reference_text='abstract'):
    query = {"query": {"bool": {"must": [
                {"term": {"reference_text":reference_text}},
                {"nested": {
                  "path": "insights",
                  "query": {"term": {"insights.dim_reduction_method": dim_reduction_method}}
                }},
                {"nested": {
                  "path": "insights.clustering_information",
                  "query": {"term": {"insights.clustering_information.clustering_method": clustering_method}}
                }},
                {"range": {"articleDate": {"gte": min_date, "lte": max_date}}}
            ]}}}
    return query


def sort_group_by_key(data,group_key):
    data.sort(key=lambda item:item['data']['articleDate'])  
    result = []
    for key, items in groupby(data, key=lambda x: x['data'][group_key]):  
        result.append({'id':key, 'level':group_key, 'elements':list(items)})
    return result


def calculate_group_key(start_date,end_date):
    date_format = "%Y-%m-%d"
    sd = datetime.strptime(start_date, date_format)
    ed = datetime.strptime(end_date, date_format)

    delta = ed - sd
    data_amount = delta.days+1

    if data_amount>365:
        group_key = 'year'
    elif data_amount>91:
        group_key = 'quarter'
    elif data_amount>31:
        group_key = 'month'
    elif data_amount>7:
        group_key = 'week'
    else:
        group_key = 'articleDate'

    return group_key


def get_year_month_quarter_and_week(date_str):
    date_format = "%Y-%m-%d"
    date_obj = datetime.strptime(date_str, date_format)
    
    quarter = (date_obj.month - 1) // 3 + 1
    week = date_obj.isocalendar()[1]

    time_levels = {'year': date_obj.year, 
                   'month': date_obj.month,
                   'quarter':f"{date_obj.year}-{quarter}",
                   'week':week,
                   'articleDate':date_str}
    
    return time_levels


def generate_groups(start_date, end_date, group_key):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    current_date = start_date

    groups = {}
    while current_date <= end_date:
        current_date_str = current_date.strftime('%Y-%m-%d')
        time_levels = get_year_month_quarter_and_week(current_date_str)
        if time_levels[group_key] not in groups.keys():
            groups[time_levels[group_key]]=[]

        groups[time_levels[group_key]].append(current_date_str)
        current_date += timedelta(days=1)

    elements_groups = []
    for group_id, dates in groups.items():
        elements_groups.append({'id':group_id,'level':group_key,'elements':[],
                                'start_date':dates[0],'end_date':dates[-1]})
        
    return elements_groups


def transform_item_to_element(item):
    label = item['_source']['insights'][0]['clustering_information'][0]['label']
    color = colors_new_legend[label]
    topic = topics_new_legend[label]
    time_levels = get_year_month_quarter_and_week(item['_source']['articleDate'])
    
    element = {'data': {'id':item['_id'].split(":")[1],'color':color,'topic':topic,
                        'articleDate':item['_source']['articleDate'],
                        'year': time_levels['year'],
                        'month': time_levels['month'],
                        'quarter':time_levels['quarter'],
                        'week':time_levels['week']},
                'position':{'x':item['_source']['insights'][0]['reduced_dimension'][0],
                            'y':item['_source']['insights'][0]['reduced_dimension'][1]}
                }
    
    return element

