from elasticsearch import Elasticsearch

# Elasticsearch连接信息
USERNAME = "elastic"
PASSWORD = "RFMNq7vG032vtpDxzVSW"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

index_name = "newsina_index"  # 需要查询的索引名称


def realPhraseSearch(query: str):
    """
    执行短语查询，返回匹配的结果。

    :param query: 要查询的短语
    :return: Elasticsearch 查询的结果
    """

    # 构建短语查询的DSL请求体
    dsl = {
        "query": {
            "multi_match": {
                "query": query,  # 查询的短语
                "fields": ["title", "keywords", "content"],  # 需要匹配的字段
                "type": "phrase",  # 短语匹配类型
                "analyzer": "ik_max_word"  # 使用 ik_max_word 分词器进行短语查询
            }
        },
        "highlight": {
            "fields": {
                "title": {},  # 高亮显示title字段
                "keywords": {},  # 高亮显示keywords字段
                "content": {}  # 高亮显示content字段
            },
            "pre_tags": ["<highlight>"],  # 高亮标签
            "post_tags": ["</highlight>"]
        }
    }

    # 执行查询
    try:
        result = es.search(index=index_name, body=dsl, size=10)  # 限制最多返回10个结果
        return result
    except Exception as e:
        return {"error": str(e)}
