from platforms import BaseFunctions, DefaultValues
import re
import json


def start(url):
    interface = 'https://c.mp.qq.com/cgi-bin/comment/Aggregation'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        item = {}
        reg = r'-(.*?).html'
        article_id = "".join(re.findall(reg, url))
        form_data = {
            'article_id': f'{article_id}',
            'cmd[]': 'articleInfo'
        }

        response = BaseFunctions.requests().post(interface, headers=headers, data=form_data, proxies=DefaultValues.proxies)
        data = json.loads(response.text)

        item['comments'] = int(data['data']['articleInfo']['data']['comment_count'])
        item['like_count'] = int(data['data']['articleInfo']['data']['like_count'])
        item['views'] = None
        item['forwards'] = None
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.result_path)
    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)