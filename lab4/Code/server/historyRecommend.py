from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 提取用户历史搜索中的关键词
def extract_frequent_keywords(user_history):
    keywords = []
    for search in user_history:
        keywords.extend(search['search_text'].split())
    return keywords


# 计算查询与用户历史内容之间的相似度
def calculate_similarity(query, user_history, results):
    # 将查询与用户历史合并，进行向量化
    vectorizer = CountVectorizer().fit_transform([query] + user_history)
    query_vec = vectorizer[0:1]  # 当前查询
    history_vecs = vectorizer[1:]  # 用户历史查询内容

    similarities = []
    for hit in results:
        doc_content = hit['_source']['content']  # 对文档的内容进行相似度计算
        doc_vec = vectorizer.transform([doc_content])

        # 计算文档与用户历史之间的余弦相似度
        similarity = cosine_similarity(doc_vec, history_vecs)
        similarities.append(similarity)

    return similarities
