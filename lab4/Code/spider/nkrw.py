import requests
from bs4 import BeautifulSoup
import random
import json
import re
import jieba

import re

def clean_keywords(keywords):
    # 去除所有非汉字字符（包括符号，标点等）
    cleaned_keywords = re.sub(r'[^\u4e00-\u9fa5]', '', keywords)
    return cleaned_keywords


# 翻页
def get_next_page_url(current_url):
    # 正则表达式提取 URL 中的数字部分
    match = re.search(r'_(\d+)\.shtml$', current_url)
    if match:
        # 获取当前页面的数字部分
        current_number = int(match.group(1))
        # 计算下一页的数字（递减 1）
        next_number = current_number - 1
        # 使用 zfill 保证数字格式一致
        next_number_str = str(next_number).zfill(len(match.group(1)))  # 保持前导零
        # 构造下一页的 URL
        next_url = current_url.replace(match.group(1), next_number_str)
        print(next_number)
        return next_url
    return None

# 定义一个函数用于提取新闻列表
def get_news_links(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # 设置正确的编码方式
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取所有新闻链接
    news_links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if 'system' in href:
            full_url = 'http://news.nankai.edu.cn' + href if href.startswith('/') else href
            news_links.append(full_url)

    return news_links

# 定义一个函数用于提取每篇新闻的详细内容
def get_news_content(url,page_links):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取各个字段，如果没有找到则填充为 "无"
    # 提取新闻来源和发稿时间
    source_time_td = soup.find('td', style="text-align:center; border-bottom:1px solid #ddd; padding-bottom:15px;")
    if source_time_td:
        # 提取新闻来源（南开新闻网）
        media_name = source_time_td.find('span', text=re.compile('来源：')).get_text(strip=True).replace('来源：', '') if source_time_td.find('span', text=re.compile('来源：')) else "无"
        # 提取发稿时间
        ctime = source_time_td.find('span', text=re.compile('发稿时间：')).get_text(strip=True).replace('发稿时间：', '') if source_time_td.find('span', text=re.compile('发稿时间：')) else "无"
    else:
        media_name = "无来源"
        ctime = "2000-1-1 00:00"

    wapurl = soup.find('meta', {'name': 'wapurl'})  # 移动端 URL
    wapurl = wapurl['content'] if wapurl else "www.none.cn"

    # 提取新闻标题
    # 提取新闻标题
    title_td = soup.find('td', style=re.compile(r'font-size:30px.*font-weight:bold.*text-align:center.*'))
    title = title_td.get_text(strip=True) if title_td else "无"

    content = ''
    for p in soup.find_all('p'):  # 新闻内容
        content += p.get_text(strip=True) + ' '
    content = content.strip() if content else "无内容"

    page_link = soup.find('a', {'class': 'page_link'})  # 相关新闻
    page_link = page_link['href'] if page_link else "无相关新闻"

    # 使用jieba分词并选取前几个关键词
    cleaned_title = clean_keywords(title)
    keywords = ' '.join(list(jieba.cut(cleaned_title))[:3])  # 使用jieba分词并取前五个词

    return {
        'ctime': ctime,
        'url': url,
        'wapurl': wapurl,
        'title': title,
        'media_name': media_name,
        'keywords': keywords,
        'content': content,
        'page_link': page_links
    }

# 定义主爬虫函数
def crawl_nankai_news():
    base_url = 'https://news.nankai.edu.cn/nkrw/system/count//0008000/000000000000/000/000/c0008000000000000000_000000067.shtml'
    all_news = []
    next_page_url = base_url

    while next_page_url:
        # 获取新闻链接
        print("已跳转到下一页")
        news_links = get_news_links(next_page_url)

        # 遍历新闻链接，抓取详细内容
        for link in news_links:
            print(f"正在抓取：{link}")
            # 随机选择 3 条新闻链接
            if len(news_links) >= 3:
                page_links = random.sample(news_links, 3)
            else:
                page_links = news_links  # 如果新闻链接少于 3 条，则直接使用所有新闻链接
            news_data = get_news_content(link,page_links)
            all_news.append(news_data)

        # 获取下一页的 URL
        next_page_url = get_next_page_url(next_page_url)

    # 将抓取的数据保存为 JSON 文件
    with open('nankai_news_nkrw.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)

    print("抓取完成，数据已保存到 nankai_news.json")

# 启动爬虫
if __name__ == '__main__':
    crawl_nankai_news()
