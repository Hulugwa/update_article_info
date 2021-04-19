from update_article_info.utils import BaseFunctions, DefaultValues
from lxml import etree


def vmall(url):
    item = {}

    try:
        response = BaseFunctions.requests().get(url, verify=False, proxies=DefaultValues.proxies, timeout=DefaultValues.timeout)
        html = etree.HTML(response.text)
        views = int(html.xpath("//span[@title='查看']/text()")[0])
        comments = int(html.xpath("//span[@title='回复']/text()")[0])

        item['url'] = url
        item['views']= views
        item['comments'] = comments
        item['forwards'] = None
        item['likes'] = None

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)