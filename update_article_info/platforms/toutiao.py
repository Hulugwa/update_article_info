from update_article_info.utils import BaseFunctions, DefaultValues
import re
import json


def toutiao(url):
    source_url = 'https://www.toutiao.com/article/v2/tab_comments/?group_id={article_id}'
    article_id = "".join(re.findall(r'\d+', url))

    try:
        response = BaseFunctions.requests().get(source_url.format(article_id=article_id), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)
        comments = int(json.loads(response.text)['total_number'])

        item = {}

        item['url'] = url
        item['forwards'] = None
        item['comments'] = comments
        item['likes'] = None
        item['views'] = None

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)