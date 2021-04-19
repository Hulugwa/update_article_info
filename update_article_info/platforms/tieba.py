from update_article_info.utils import BaseFunctions, DefaultValues
from lxml import etree


def start(url):
    item = {}
    try:
        response = BaseFunctions.requests().get(url, verify=False, proxies=DefaultValues.proxies, timeout=DefaultValues.timeout)
        html = etree.HTML(response.text)

        comments = int("".join(html.xpath("//*[@id='thread_theme_5']//span[@style='margin-right:3px']/text()")))

        item['url'] = url
        item['comments'] = comments
        item['forwards'] = None
        item['likes'] = None
        item['views'] = None

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)