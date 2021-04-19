from update_article_info.utils import BaseFunctions, DefaultValues
import re
import json


def start(url):
    source_get_itemId_url = 'https://ff.dayu.com/contents/{article_id}?biz_id=1002'
    source_comment_url = 'http://m.uczzd.cn/iflow/api/v2/cmt/article/{item_id}/comments/byhot'
    item = {}

    try:
        if 'm.uczzd.cn' in url or 'iflow.uc.cn' in url:
            item_id = "".join(re.findall(r'aid=(.*)', url))
        elif 'a.mp.uc.cn' in url:
            article_id = "".join(re.findall(r'cid=(.*)', url))
            item_response = BaseFunctions.requests().get(source_get_itemId_url.format(article_id=article_id), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)
            item_id = json.loads(item_response.text)['data']['_extra']['xss_item_id']
        else:
            pass

        comment_response = BaseFunctions.requests().get(source_comment_url.format(item_id=item_id), verify=False, timeout=DefaultValues.timeout, proxies=DefaultValues.proxies)
        data = json.loads(comment_response.text)

        comments = data['data']['comment_cnt']
        likes = data['data']['like_cnt']

        item['url'] = url
        item['comments'] = comments
        item['forwards'] = None
        item['likes'] = likes
        item['views'] = None

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)