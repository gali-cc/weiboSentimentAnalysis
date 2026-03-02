import csv
import os
import requests
import numpy as np

csv_path = os.path.join(os.path.dirname(__file__), 'arcType_data.csv')

def init_csv():
    if os.path.exists(csv_path):
        exit("arcType_data.csv文件已存在, 无需初始化")

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            '类别标题(title)',
            '分组id(gid)',
            '分类id(containerid)',
        ])

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

def parseJson(json_data):
    if json_data and 'groups' in json_data:
        arcTypeList = np.append(json_data['groups'][3]['group'], json_data['groups'][4]['group'])
        for item in arcTypeList:
            title = item.get('title', '')
            gid = item.get('gid', '')
            containerid = item.get('containerid', '')
            print(f"标题: {title}, 分组id: {gid}, 分类id: {containerid}")
            with open(csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([title, gid, containerid])

def start():
    init_csv()
    url = "https://weibo.com/ajax/feed/allGroups"
    params = {
        "is_new_segment": "1",
        "fetch_hot": "1",
    }
    json_data = getJsonHtml(url, {})
    parseJson(json_data)

if __name__ == '__main__':
    start()
