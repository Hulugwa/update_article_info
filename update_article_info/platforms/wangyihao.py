from update_article_info.utils import BaseFunctions, DefaultValues
import re
import json


def wangyi(url):
    article_id = "".join(re.findall(r'.*/(.*).html', url))
    source_url = 'https://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{article_id}'

    try:
        response = BaseFunctions.requests().get(source_url.format(article_id=article_id), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)

        likes = int(json.loads(response.text)['cmtCount'])
        forwards = int(json.loads(response.text)['rcount'])
        comments = int(json.loads(response.text)['tcount'])

        item = {}

        item['url'] = url
        item['comments'] = comments
        item['forwards'] = forwards
        item['likes'] = likes
        item['views'] = None

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)