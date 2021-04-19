from update_article_info.utils import BaseFunctions, DefaultValues
import re
import json


def start(url):
    try:
        if 'read' in url:
            bbRead(url)
        if 'video' in url:
            bbVideo(url)
    except:
        pass


def bbRead(url):
    source_url = 'https://api.bilibili.com/x/article/viewinfo?id={id}'

    try:
        item = {}
        reg = r'read/cv(.*)'
        id = "".join(re.findall(reg, url))
        request_url = source_url.format(id=id)

        response = BaseFunctions.requests().get(request_url, verify=False, proxies=DefaultValues.proxies)
        data = json.loads(response.text)

        item['views'] = int(data['data']['stats']['view'])
        item['likes'] = int(data['data']['stats']['like'])
        item['comments'] = int(data['data']['stats']['reply'])
        item['forwards'] = int(data['data']['stats']['share'])
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)

def bbVideo(url):
    source_url = 'https://api.bilibili.com/x/web-interface/view/detail?aid={aid}&bvid={bvid}'

    try:
        item = {}
        reg = r'/video/(.*)'
        id = "".join(re.findall(reg, url))

        if 'av' in id:
            request_url = source_url.format(aid=id.replace('av', ''), bvid='')
        else:
            request_url = source_url.format(aid='', bvid=id)

        response = BaseFunctions.requests().get(request_url, verify=False, proxies=DefaultValues.proxies)
        data = json.loads(response.text)

        views = int(data['data']['View']['stat']['view'])
        comments = int(data['data']['View']['stat']['reply'])
        likes = int(data['data']['View']['stat']['like'])
        forwards = int(data['data']['View']['stat']['share'])

        item['views'] = views
        item['comments'] = comments
        item['likes'] = likes
        item['forwards'] = forwards
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)