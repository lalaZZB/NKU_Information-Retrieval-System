import webbrowser
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from search import search
from wildcardSearch import wildcardSearch
from phraseSearch import phraseSearch
from realPhraseSearch import realPhraseSearch
import documentSearch
import logging
from elasticsearch import Elasticsearch
import json

# 连接到Elasticsearch
USERNAME = "elastic"
PASSWORD = "RFMNq7vG032vtpDxzVSW"
es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='./search_logs.log', level=logging.INFO)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"
user_search_history = {}
SEARCH_HISTORY_FILE = 'search_history.txt'


# 定义文档索引的路由
@app.route('/index-documents', methods=['POST'])
def index_documents_route():
    try:
        documentSearch.index_documents()
        return jsonify({"message": "Documents indexed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 定义搜索功能的路由
@app.route('/search-documents', methods=['GET'])
def search_documents_route():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400
    try:
        results = documentSearch.search_documents(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-search-history', methods=['GET'])
def get_search_history():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        # 如果文件存在，则读取搜索历史记录
        if os.path.exists(SEARCH_HISTORY_FILE):
            with open(SEARCH_HISTORY_FILE, 'r') as file:
                file_data = json.load(file)
                user_history = file_data.get(username, [])
                return jsonify({'history': user_history}), 200
        else:
            return jsonify({'history': []}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch search history', 'details': str(e)}), 500

@app.route('/store-search-history', methods=['POST'])
def store_search_history():
    data = request.json
    username = data['username']
    search_text = data['searchText']

    # 如果用户已经有存储的搜索历史，则追加到它的列表中
    if username in user_search_history:
        user_search_history[username].append(search_text)
    else:
        user_search_history[username] = [search_text]

    # 将搜索历史保存到文本文件中
    try:
        # 读取现有的搜索历史（如果文件存在）
        if os.path.exists(SEARCH_HISTORY_FILE):
            with open(SEARCH_HISTORY_FILE, 'r') as file:
                file_data = json.load(file)
        else:
            file_data = {}

        # 更新文件数据
        file_data[username] = user_search_history[username]
        print("已将搜索记录存入历史文件中")

        # 写入文件
        with open(SEARCH_HISTORY_FILE, 'w') as file:
            json.dump(file_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        # 如果出现异常，返回错误消息
        return jsonify({'error': 'Failed to save search history', 'details': str(e)}), 500

    return jsonify({'message': 'Search history saved successfully.'}), 200


@app.route('/login', methods=['POST'])
def login():
    # 获取JSON数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(username, password)

    # 校验用户名和密码
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # 登录成功，返回成功消息
        return jsonify({'message': 'Login successful'}), 200
    else:
        # 登录失败，返回错误消息
        return jsonify({'error': '用户名或者密码输入错误！'}), 401


@app.route('/open-snapshot', methods=['GET'])
def open_snapshot():
    image_name = request.args.get('image_name', '')
    
    if image_name:
        # 指向 snapshot 文件夹中的 resized_snapshot_img
        image_path = '../snapshot/resized_snapshot_img/' + image_name + '.png'

        # 打开图片
        try:
            webbrowser.open('file://' + os.path.abspath(image_path))
            print("完整路径:", os.path.abspath(image_path))
            return jsonify({'message': f'Snapshot opened for {image_name}'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No image name provided'}), 400

@app.route('/get-recommendations', methods=['GET'])
def get_recommendations():
    news_id = request.args.get('id', '')

    print("news_id: ", news_id)
    if not news_id:
        return jsonify({'error': 'No news ID provided'}), 400

    try:
        # 查询 Elasticsearch 获取推荐新闻
        res = es.get(index='newsina_index', id=news_id)
        print("res: ", res)
        if res['found']:
            print("正在访问推荐列表")
            # 直接访问 '_source' 中的 'recommend' 字段，它已经是一个列表了
            recommendations = res['_source'].get('recommend', [])
            print(f"推荐列表: {recommendations}")  # 打印推荐列表
            return jsonify({'recommendations': recommendations})
        else:
            return jsonify({'error': 'News not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['GET'])
def searchs():
    print("已调用搜索函数")
    text = request.args.get('q', '')
    wildcard = request.args.get('wildcard', 'false') == 'true'
    phrase = request.args.get('phrase', 'false') == 'true'
    realPhrase = request.args.get('realPhraseSearch', 'false') == 'true'
    if text:
        if phrase:
            # 直接获取短语搜索的参数
            keywords = request.args.get('keywords', '')
            startDate = request.args.get('startDate', '')
            endDate = request.args.get('endDate', '')
            media = request.args.get('media', '')
            excluded_content = request.args.get('excludedContent', '')
            # print(text, keywords, startDate, endDate, media, excluded_content)
            # 短语搜索
            result = phraseSearch(text, keywords, startDate, endDate, media, excluded_content)
        elif wildcard:
            # 通配符搜索
            result = wildcardSearch(text)
        elif realPhrase:
            # 真正的短语查询
            # 直接获取短语搜索的参数
            keywords = request.args.get('keywords', '')
            startDate = request.args.get('startDate', '')
            endDate = request.args.get('endDate', '')
            media = request.args.get('media', '')
            excluded_content = request.args.get('excludedContent', '')
            result = realPhraseSearch(text)
        else:
            # 标准搜索
            print("已调用标准搜索函数")
            result = search(text)

        # 记录日志
        log_data = {
            'text': text,
            'keywords': keywords if phrase else '',
            'startDate': startDate if phrase else '',
            'endDate': endDate if phrase else '',
            'media': media if phrase else '',
            'excluded_content': excluded_content if phrase else '',
            'result': [{'url': hit['_source']['url'], 'title': hit['_source']['title']} for hit in result['hits']['hits']]
        }
        print("已记录日志")
        logging.info(log_data)
        # 检查 result 是否为预期格式
        if 'hits' not in result or 'hits' not in result['hits']:
            print("已检查result，不符合预期格式")
            return jsonify({'error': 'Invalid search results format'}), 500
        print("已检查result，符合预期格式")
        print("已返回搜索结果！")
        return jsonify(result['hits']['hits'])
    else:
        return jsonify({'error': 'No query provided'}), 400

if __name__ == "__main__":
    app.run(debug=True)
