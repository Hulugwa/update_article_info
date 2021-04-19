from update_article_info.utils import BaseFunctions, DefaultValues
import re
import json


def start(url):
    item = {}
    comment_source_url = 'https://coral.qq.com/article/{target_id}/commentnum'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    try:
        if 'rain' in url:
            request_url = url
        elif 'cmsid' in url:
            request_url = 'https://new.qq.com/rain/a/' + "".join(re.findall(r'cmsid=(.*)', url))
        elif 'omn' in url:
            response_url = BaseFunctions.requests().get(url, verify=False, proxies=DefaultValues.proxies,timeout=DefaultValues.timeout).url
            if 'notfound.htm' in response_url:
                end_str = re.match(r'http(.*)/(.*)', url).group(2)
                article_id = end_str.replace("".join(re.findall(r'(\..*)', end_str)), '')
                request_url = 'https://new.qq.com/rain/a/' + article_id
            else:
                request_url = url

        else:
            pass

        # 获取target_id
        response = BaseFunctions.requests().get(request_url, verify=False, proxies=DefaultValues.proxies, timeout=DefaultValues.timeout)
        target_id = "".join(re.findall(r'comment_id": "(.*)",', response.text))

        # 通过target_id构造请求url获取评论数
        comment_response = BaseFunctions.requests().get(comment_source_url.format(target_id=target_id), proxies=DefaultValues.proxies, verify=False, timeout=DefaultValues.timeout, headers=headers)
        comments = json.loads(comment_response.text)['data']['commentnum']

        item['url'] = url
        item['comments'] = comments
        item['forwards'] = None
        item['likes'] = None
        item['views'] = None

        BaseFunctions.writeFile(item, DefaultValues.item_path)
    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)