from platforms import BaseFunctions, DefaultValues
import re
import json
import traceback


def start(url):
    try:
        if '3g.k.sohu' in url:
            souhu3g(url)
        if 'www.sohu.com' in url:
            msouhu(url)
        else:
            pass

    except:
        pass


def souhu3g(url):
    source_url = 'https://3g.k.sohu.com/api/comment/getCommentListByCursor.go?id={id}&busiCode=2'

    try:
        item = {}
        reg = r'/n(.*)'
        id = "".join(re.findall(reg, url))
        response = BaseFunctions.requests().get(source_url.format(id=id), timeout=DefaultValues.timeout, verify=False, proxies=DefaultValues.proxies)

        data = json.loads(response.text)

        comments = int(data['response']['totalCount'])

        item['comments'] = comments
        item['likes'] = None
        item['views'] = None
        item['forwards'] = None

        BaseFunctions.writeFile(item, DefaultValues.result_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)


def msouhu(url):
    source_url = 'https://api.interaction.sohu.com/api/comments/maincomments?source_id=mp_{id}&reply_count=1&page_size=1&type=0&page_no=1'

    try:
        item = {}

        reg = r'www.sohu.com/.*/(.*?)_'
        id = "".join(re.findall(reg, url))
        response = BaseFunctions.requests().get(source_url.format(id=id), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)

        data = json.loads(response.text)
        comments = int(data['data']['totalCount'])

        item['comments'] = comments
        item['likes'] = None
        item['views'] = None
        item['forwards'] = None
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.result_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)
