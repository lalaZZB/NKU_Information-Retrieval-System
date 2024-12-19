from elasticsearch import Elasticsearch
import os
import json
USERNAME = "elastic"
PASSWORD = "RFMNq7vG032vtpDxzVSW"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

index_name = "newsina_index"

# ...其他代码...

def search(query: str):
    dsl = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "keywords", "content"],
                            "type": "best_fields",
                            "analyzer": "ik_smart",  # 使用 ik_smart 分词器
                            "tie_breaker": 0.3
                        }
                    },
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "keywords", "content"],
                            "type": "phrase",
                            "analyzer": "ik_max_word"  # 使用 ik_max_word 分词器进行短语搜索
                        }
                    }
                ]
            }
        },
        "highlight": {
            "fields": {
                "title": {},
                "keywords": {},
                "content": {}
            },
            "require_field_match": False,
            "pre_tags": ["<highlight>"],
            "post_tags": ["</highlight>"]
        }
    }
    # 提取历史搜索记录
    if os.path.exists('search_history.txt'):
        with open('search_history.txt', 'r') as file:
            file_data = json.load(file)
            user_history = file_data.get("admin", [])
            # 如果有历史记录，返回第一个搜索词
            if user_history:
                history_keyword = user_history[0]  # 返回历史搜索记录中的第一个词
                print(history_keyword)

    # 如果有历史搜索中的第一个关键词，则将其加入到查询中，权重较低
    if history_keyword:
        dsl["query"]["bool"]["should"].append({
            "multi_match": {
                "query": history_keyword,
                "fields": ["title", "keywords", "content"],
                "type": "best_fields",
                "analyzer": "ik_smart",  # 使用相同的分词器
                "boost": 0.1  # 设置较低的权重，0.1意味着低优先级
            }
        })

    result = es.search(index=index_name, body=dsl, size=20)
    return result