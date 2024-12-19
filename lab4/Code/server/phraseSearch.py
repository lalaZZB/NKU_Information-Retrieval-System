from elasticsearch import Elasticsearch
from datetime import datetime

# Elasticsearch 连接配置
USERNAME = "elastic"
PASSWORD = "RFMNq7vG032vtpDxzVSW"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

index_name = "newsina_index"


def phraseSearch(text, keywords, startDate, endDate, media, excluded_content):
    # 构建短语查询
    query = {
        "bool": {
            "must": [],
            "filter": [],
            "must_not": []
        }
    }

    # 添加文本搜索条件
    if text:
        query["bool"]["must"].append({"match_phrase": {"content": text}})

    # # 添加关键词条件
    # if keywords:
    #     query["bool"]["must"].append({"match": {"keywords": keywords}})

    # 添加日期范围条件
    if startDate and endDate:
        query["bool"]["filter"].append({
            "range": {
                "ctime.keyword": {
                    "gte": startDate,
                    "lte": endDate,
                    "format": "yyyy-MM-dd"

                }
            }
        })
    print("已添加日期范围条件")
    # 添加媒体名称条件
    if media:
        query["bool"]["must"].append({"match": {"media_name": media}})

    # 添加排除内容条件
    if excluded_content:
        query["bool"]["must_not"].append({"match": {"content": excluded_content}})

    # 执行查询
    response = es.search(index=index_name, body={"query": query})
    print("已执行短语查询")
    # 返回结果
    return response

# 示例调用
# result = phraseSearch("游戏", "网易", "2023-01-01", "2023-12-31", "环球网", "政治")
# print(result)
