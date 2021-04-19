from update_article_info.utils import BaseFunctions, DefaultValues
import json
import re
from lxml import etree


def start(url):
    item = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    try:

        response = BaseFunctions.requests().get(url, verify=False, proxies=DefaultValues.proxies, timeout=DefaultValues.timeout, headers=headers)

        html = etree.HTML(response.text)

        views_str = "".join(html.xpath("//div[@class='QuestionFollowStatus']//div[@class='NumberBoard-item'][2]//strong/text()")).replace(',', '')
        views = 0 if views_str == '' else int(views_str)

        if 'answer' in url:
            answer_id = re.findall(r'answer/(\d+)', url)[0]
            data = json.loads(re.findall(r'answers"\s*:(.*?),\s*"articles"', response.text)[0])

            comments = data[answer_id]['commentCount']
            likes = data[answer_id]['voteupCount']
        else:
            likes_str = "".join(html.xpath("//div[@class='List-item'][1]/div[1]/meta[2]/@content"))
            comments_str = "".join(html.xpath("//div[@class='List-item'][1]/div[1]/meta[6]/@content"))

            likes = 0 if likes_str == '' else int(likes_str)
            comments = 0 if comments_str == '' else int(comments_str)

        item['url'] = url
        item['comments'] = comments
        item['likes'] = likes
        item['forwards'] = None
        item['views'] = views

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:

        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)



