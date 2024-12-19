import os
from elasticsearch import Elasticsearch
from docx import Document
import fitz  # PyMuPDF
import pandas as pd

# 初始化 Elasticsearch 客户端
USERNAME = "elastic"
PASSWORD = "RFMNq7vG032vtpDxzVSW"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

index_name = "documents_index"


# 提取文档内容
def extract_content(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    content = ""

    if extension == ".docx":
        doc = Document(file_path)
        content = "\n".join([para.text for para in doc.paragraphs])
    elif extension == ".pdf":
        pdf = fitz.open(file_path)
        for page in pdf:
            content += page.get_text() + "\n"
        pdf.close()
    elif extension in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
        content = df.to_string(index=False)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

    return content


# 索引文档
def index_documents(directory="document"):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        try:
            content = extract_content(file_path)
            doc = {
                "file_name": file_name,
                "content": content
            }
            es.index(index=index_name, document=doc)
            print(f"Indexed: {file_name}")
        except Exception as e:
            print(f"Failed to index {file_name}: {e}")


# 搜索文档
def search_documents(query):
    dsl = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["content"],
                "type": "best_fields",
                "analyzer": "standard"
            }
        },
        "highlight": {
            "fields": {
                "content": {
                    "pre_tags": ["<em>"],
                    "post_tags": ["</em>"]
                }
            }
        }
    }

    result = es.search(index=index_name, body=dsl, size=10)
    hits = result.get('hits', {}).get('hits', [])
    search_results = []
    for hit in hits:
        search_results.append({
            "file_name": hit['_source']['file_name'],
            "content": hit['_source']['content'][:200],  # 返回前 200 个字符作为预览
            "highlight": hit.get('highlight', {}).get('content', [])
        })
    return search_results
