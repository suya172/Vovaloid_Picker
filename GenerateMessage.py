import requests
import json
from datetime import date, timedelta
import random


def get_json(url):
    today = date.today()
    yesterday = today-timedelta(1)

    try:
        res = requests.get(
            url,
            params={
                "q": "vocaloidオリジナル曲",
                "targets": "tagsExact",
                "fields": "contentId,title",
                "filters[startTime][gte]": f"{yesterday.isoformat()}T00:00:00+09:00",
                "filters[startTime][lt]": f"{today.isoformat()}T00:00:00+09:00",
                "_sort": "startTime",
                "_context": "vocaloid_everyday"
            }
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\033[31mError:{e}\033[0m")
        return json.dumps({'meta': {'status': 000}})
    else:
        print("\033[33m取得完了\033[0m")

    data = res.json()
    return data


def create_message(url='https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search'):
    data = get_json(url=url)
    status = data['meta']['status']
    message = f'エラー： HTTPステータスコード{status}'
    if status == 000:
        message = 'エラー：通信に失敗しました。'
    elif status == 400:
        message = 'エラー：パラメータが不正です。'
    elif status == 500:
        message = 'エラー：検索サーバに異常が発生しています。'
    elif status == 503:
        message = 'エラー：サービスがメンテナンス中です。'
    elif status == 200:
        contents_array = data['data']
        pick_content = random.choice(contents_array)
        Id = pick_content['contentId']
        title = pick_content['title']
        message = f'今日の新着ボカロ曲だよ！\n\n{title}\nhttps://www.nicovideo.jp/watch/{Id}'
    return message
