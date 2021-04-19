from update_article_info.utils import BaseFunctions, DefaultValues
import re
import json


def start(url):
    source_url = 'https://kuaibao.qq.com/getSubNewsContent?id={article_id}'
    item = {}

    try:
        article_id = "".join(re.findall(r's/(.*)', str(url).replace("".join(re.findall(r'(\?.*)', url)), '')))
        response = BaseFunctions.requests().get(source_url.format(article_id=article_id), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)

        data = json.loads(response.text)
        comments = data['count_info']['comments']
        likes = data['count_info']['like_info']

        item['url'] = url
        item['comments'] = comments
        item['likes'] = likes
        item['forwards'] = None
        item['views'] = None

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:

        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)
