from platforms import BaseFunctions, DefaultValues
import re
import json
import traceback


def start(url):
    source_url = 'https://api.interaction.sohu.com/api/comments/maincomments?source_id=mp_{id}&reply_count=1&page_size=1&type=0&page_no=1'

    try:
        item = {}

        id = "".join(re.findall(r'/a/(.*)_', url))
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
