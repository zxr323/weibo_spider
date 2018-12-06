import requests

url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/1270468784',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5\
     Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3464.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(page):
    params = {
        'type': 'uid',
        'value': '1270468784',
        'containerid': '1076031270468784',
        'page': page
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


from pyquery import PyQuery as pq


def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            try:
                item = item.get('mblog')
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()   #通过pyquery去掉text中的标签
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                yield weibo
            except:
                return None


if __name__ == '__main__':
    for page in range(1, 11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)

