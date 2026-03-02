import csv
from datetime import datetime
import os
import time

import requests

from weiboanalysis.util.stringUtil import clean_string


def init_csv():
    csv_path = os.path.join(os.path.dirname(__file__), 'comment_data.csv')
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id',
                'text_raw',
                'created_at',
                'source',
                'like_counts',
                'articleId',
                'userId',
                'userName',
                'gender',
                'userHomeUrl'
            ])

def getAllArticleList():
    csv_path = os.path.join(os.path.dirname(__file__), 'article_data.csv')
    with open(csv_path, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)
        articleList = [row for row in reader]
    return articleList

def getJsonHtml(url, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'cookie': "SUB=_2AkMfM2pmf8NxqwFRmfwQym3gaYt-zwvEieKpb5u9JRMxHRl-yj9kqlYFtRB6NLNEiTHDYf6iUJpzyFGO_5YK2MlqVYFo; XSRF-TOKEN=bAvtgoyXhdYRDFBs_eXumhun; WBPSESS=Wk6CxkYDejV3DDBcnx2LOQZ-emQTpI4uumku6j7pHnnOz_YcA_MlkusG-mHzVlV4xhkBIogTJMIFM-yzMPUBM0IyZyMFBnhQFRd2Prg3jSqmM3ytBNs5gq6K6rM7whxQN7cSM7NLEGElAW-Jj1Pxq3YvvJ5rRE1F9_mZiXSIpEs=",
        'Referer': 'https://weibo.com/',
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败, 状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def parseJson(json_data, articleId):
    commentList = json_data.get('data', [])
    for comment in commentList:
        id = comment.get('id', '')
        text_raw = clean_string(comment.get('text_raw', ''))
        created_at = datetime.strptime(comment.get('created_at', ''), "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S")
        source = comment.get('source', '').replace('来自', '').strip()
        like_counts = comment.get('like_counts', 0)

        user = comment.get('user', {})
        userId = user.get('id', '')
        userName = user.get('screen_name', '')
        gender = '男' if user.get('gender', '').strip() == 'm' else '女'
        userHomeUrl = f"https://weibo.com{user.get('profile_url', '')}"

        filePath = os.path.join(os.path.dirname(__file__), 'comment_data.csv')
        with open(filePath, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                id,
                text_raw,
                created_at,
                source,
                like_counts,
                articleId,
                userId,
                userName,
                gender,
                userHomeUrl
            ])


def start():
    url = 'https://weibo.com/ajax/statuses/buildComments'
    init_csv()
    articleList = getAllArticleList()

    print("==========微博内容爬取开始==========")
    for article in articleList:
        print(f"正在获取【{article[1]}】的评论内容......")
        time.sleep(1)
        params = {
            'id': article[0],
            'is_show_bulletin': 2,
        }
        json_data = getJsonHtml(url, params)
        if json_data:
            parseJson(json_data, article[0])
        
    
    print("==========微博内容爬取完成==========")


if __name__ == '__main__':
    start()
