import csv
import os
import time
from datetime import datetime

import requests

from weiboanalysis.util.stringUtil import clean_string

csv_path = os.path.join(os.path.dirname(__file__), 'article_data.csv')

def init_csv():
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id',
                'text_raw',
                'reposts_count',
                'comments_count',
                'attitudes_count',
                'region_name',
                'created_at',
                'articleType',
                'articleUrl',
                'authorId',
                'authorName',
                'authorHomeUrl'
            ])

def getAllTypeList():
    csv_path = os.path.join(os.path.dirname(__file__), 'arcType_data.csv')
    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        allTypeList = [row for row in reader]
        return allTypeList
    

def getJsonHtml(url, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'cookie': "SUB=_2AkMfM2pmf8NxqwFRmfwQym3gaYt-zwvEieKpb5u9JRMxHRl-yj9kqlYFtRB6NLNEiTHDYf6iUJpzyFGO_5YK2MlqVYFo; XSRF-TOKEN=bAvtgoyXhdYRDFBs_eXumhun; WBPSESS=Wk6CxkYDejV3DDBcnx2LOQZ-emQTpI4uumku6j7pHnnOz_YcA_MlkusG-mHzVlV4xhkBIogTJMIFM-yzMPUBM0IyZyMFBnhQFRd2Prg3jSqmM3ytBNs5gq6K6rM7whxQN7cSM7NLEGElAW-Jj1Pxq3YvvJ5rRE1F9_mZiXSIpEs=",
        'Referer': 'https://weibo.com/',
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        print(response.url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败, 状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def parseJson(json_data, articleType):
    articleList = json_data.get('statuses', [])
    for article in articleList:
        id = article.get('id', '')
        text_raw = clean_string(article.get('text_raw', ''))
        reposts_count = article.get('reposts_count', 0)
        comments_count = article.get('comments_count', 0)
        attitudes_count = article.get('attitudes_count', 0)
        region_name = article.get('region_name', '').replace('发布于', '').strip()
        created_at = datetime.strptime(article.get('created_at', ''), "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S")
        articleUrl = f'https://weibo.com/{article["user"]["id"]}/{article["mblogid"]}'
        authorId = article["user"]["id"]
        authorName = article["user"]["screen_name"]
        authorHomeUrl = f'https://weibo.com/u/{article["user"]["id"]}'

        with open(csv_path, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                id,
                text_raw,
                reposts_count,
                comments_count,
                attitudes_count,
                region_name,
                created_at,
                articleType,
                articleUrl,
                authorId,
                authorName,
                authorHomeUrl
            ])
        

def start():
    url = 'https://weibo.com/ajax/feed/hottimeline'
    init_csv()

    allTypeList = getAllTypeList()
    print("==========微博内容爬取开始==========")
    for typeRow in allTypeList:
        print(f"正在获取【{typeRow[0]}({typeRow[1]})】的微博内容......")
        time.sleep(1)
        params = {
            "group_id": typeRow[1],
            "containerid": typeRow[2],
            "extparam": "discover|new_feed",
        }
        json_data = getJsonHtml(url, params)
        if json_data:
            parseJson(json_data, typeRow[0])
        else:
            print(f"获取【{typeRow[0]}({typeRow[1]})】的微博内容失败")

    print("==========微博内容爬取结束==========")

if __name__ == '__main__':
    start()
