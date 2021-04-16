from platforms import BaseFunctions, DefaultValues
import re
import json
import traceback


def yidianzixun(url):
    source_url = 'http://www.yidianzixun.com/home/q/getcomments?docid={article_id}&count=30'
    article_id = "".join(re.findall('article/(.*)', str(url).replace("".join(re.findall('(\?.*)', url)), ''))).replace('/', '')
    item = {}

    try:
        response = BaseFunctions.requests().get(source_url.format(article_id=article_id), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)
        comments = int(json.loads(response.text)['total'])

        item['url'] = url
        item['forwards'] = None
        item['comments'] = comments
        item['likes'] = None
        item['views'] = None

        BaseFunctions.writeFile(item, DefaultValues.result_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)