from platforms import BaseFunctions, DefaultValues
import json
import re
import traceback


def start(url):
    source_url = 'https://www.dongchedi.com/motor/info/ugc/short/article/v1/?group_id={article_id}&from=pc_station'

    try:
        item = {}
        article_id = "".join(re.findall(r'article/(.*)', url))
        response = BaseFunctions.requests().get(source_url.format(article_id=article_id), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)

        data = json.loads(response.text)

        comments = int(data['data']['comment_count'])
        views = int(data['data']['read_count'])
        likes = int(data['data']['digg_count'])
        forwards = int(data['data']['share_count'])

        item['url'] = url
        item['forwards'] = forwards
        item['comments'] = comments
        item['likes'] = likes
        item['views'] = views

        BaseFunctions.writeFile(item, DefaultValues.result_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)
