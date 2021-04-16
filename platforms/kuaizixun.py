from platforms import BaseFunctions, DefaultValues
import re
import json


def start(url):
    try:
        if '360kuai' in url:
            kuai360(url)
        if 'm.news.so.com' in url:
            mnews(url)
        else:
            pass
    except:
        pass


def kuai360(url):
    source_url = 'https://www.360kuai.com/user/comment/lists?f=jsonp&page_key={page_key}'

    try:
        item = {}
        page_key = "".join(re.findall(r'.com/(.*)', url))
        response = BaseFunctions.requests().get(source_url.format(page_key=page_key), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)
        data = json.loads(response.text)

        comments = int(data['data']['total'])

        item['url'] = url
        item['comments'] = comments
        item['likes'] = None
        item['forwards'] = None
        item['views'] = None

        BaseFunctions.writeFile(item, DefaultValues.result_path)

    except:
        pass

def mnews(url):
    item = {}
    source_interface = 'https://u.api.look.360.cn/comment/lists?url={param_url}'
    param_url = "".join(re.findall(r'url=(.*)', url))

    try:
        response = BaseFunctions.requests().get(source_interface.format(param_url=param_url), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)
        data = json.loads(response.text)

        comments = int(data['data']['total'])

        item['url'] = url
        item['comments'] = comments
        item['likes'] = None
        item['forwards'] = None
        item['views'] = None

        BaseFunctions.writeFile(item, DefaultValues.result_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)
