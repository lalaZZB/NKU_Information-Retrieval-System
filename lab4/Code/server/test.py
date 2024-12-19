import json
import os

def get_first_keyword_from_history(username):
    if os.path.exists('search_history.txt'):
        with open('search_history.txt', 'r') as file:
            file_data = json.load(file)
            user_history = file_data.get(username, [])
            # 如果有历史记录，返回第一个搜索词
            if user_history:
                return user_history[0]  # 返回历史搜索记录中的第一个词
    return None  # 如果没有历史记录，返回 None

# 示例调用
username = "admin"
first_keyword = get_first_keyword_from_history(username)
print("First keyword from history:", first_keyword)
