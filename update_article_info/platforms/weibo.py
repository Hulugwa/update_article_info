import re
import json
from lxml import etree
from update_article_info.utils import BaseFunctions, DefaultValues


def start(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Cookie': 'SINAGLOBAL=4813403181515.393.1614675647253; UOR=,,www.baidu.com; SUB=_2AkMXGS0Pf8NxqwJRmfsSz2PiZY9wwwHEieKhRdzUJRMxHRl-yT9kql4CtRB6PJkD4DyZKKRvisLn0T3XT1mmPjgYMP-T; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5MlfLdcaj5Hs24b9hrEZu4; login_sid_t=bb8b362aae60bcb8824d79fd69224aaf; cross_origin_proto=SSL; _s_tentry=-; Apache=4623102832203.645.1615254315211; ULV=1615254315215:3:3:2:4623102832203.645.1615254315211:1615176251737; WBtopGlobal_register_version=2021031011; wb_view_log=1440*9002%261920*10801; WBStorage=202103101503|undefined'
    }

    # http处理
    if 'http:' in str(url):
        request_url = str(url).replace('http:', 'https:')
    else:
        request_url = url

    try:
        response = BaseFunctions.requests().get(request_url, verify=False, headers=headers, proxies=DefaultValues.proxies, timeout=DefaultValues.timeout)

        detail = re.search(r'{(.*?)"domid":"Pl_Official_WeiboDetail__73"(.*?)}\)', response.text)

        if detail:
            item = {}

            data = json.loads(detail.group().replace('})', '}'))
            html = etree.HTML(data['html'], parser=etree.HTMLParser(encoding='utf-8'))

            forwards = int(html.xpath("//span[@node-type='forward_btn_text']//text()")[1]) if html.xpath("//span[@node-type='forward_btn_text']//text()")[1] != '转发' else 0
            comments = int(html.xpath("//span[@node-type='comment_btn_text']//text()")[1]) if html.xpath("//span[@node-type='comment_btn_text']//text()")[1] != '评论' else 0
            likes = int(html.xpath("//div[@node-type='feed_list_options']//span[@node-type='like_status']//text()")[1]) if html.xpath("//div[@node-type='feed_list_options']//span[@node-type='like_status']//text()")[1] != '赞' else 0

            item['url'] = url
            item['forwards'] = forwards
            item['comments'] = comments
            item['likes'] = likes
            item['views'] = None

            BaseFunctions.writeFile(item, DefaultValues.item_path)

        else:
            BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)