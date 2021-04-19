from update_article_info.utils import BaseFunctions, DefaultValues
import re
import json


def start(url):
    source_url = 'https://comment.sina.com.cn/page/info?newsid={id}&channel=mp'

    try:
        item = {}

        id = "".join(re.findall(r'article_(.*).html', url)).replace('_', '-')
        response = BaseFunctions.requests().get(source_url.format(id=id), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)

        data = json.loads(response.text)
        comments = str(data['result']['count']['total'])

        item['comments'] = comments
        item['likes'] = None
        item['views'] = None
        item['forwards'] = None
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)