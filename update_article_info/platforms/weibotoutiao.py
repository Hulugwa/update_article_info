import re
from lxml import etree
from update_article_info.utils import BaseFunctions, DefaultValues


def start(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Cookie': 'SINAGLOBAL=4813403181515.393.1614675647253; UOR=,,login.sina.com.cn; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhlR.k2GdqbjyZzEITOSHRr5JpX5KMhUgL.Foece0.0Sh2cehM2dJLoIp7LxKnL12BL1KzLxK.L1hML12H7i--fi-88i-2E; ALF=1649747641; SSOLoginState=1618211642; SCF=AgcHxrBHHt4UjbLh9mubH40GHYX5wHnmPtTAqB6TkyEecKlr459m1ZsEsdZPkpxPDP11WmTyMyb9vrmOnKIcOo8.; SUB=_2A25Nd4NqDeRhGeVI6FsS9C_KyzuIHXVuBPOirDV8PUNbmtANLXfWkW9NTAPerAbffhFF6sJAbxCl8XyTcJIKscGB; _s_tentry=login.sina.com.cn; Apache=9695619437120.088.1618211644332; ULV=1618211644356:10:3:1:9695619437120.088.1618211644332:1617702472974; wb_view_log_3639341607=1920*10801; webim_unReadCount=%7B%22time%22%3A1618211680769%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A11%2C%22msgbox%22%3A0%7D; WBStorage=8daec78e6a891122|undefined'
    }

    # http处理
    if 'http:' in str(url):
        request_url = str(url).replace('http:', 'https:')
    else:
        request_url = url

    try:
        item = {}
        response = BaseFunctions.requests().get(request_url, verify=False, headers=headers, proxies=DefaultValues.proxies, timeout=DefaultValues.timeout)

        html = etree.HTML(response.text)
        views_str = "".join(html.xpath("//div[@class='W_fr']//text()"))
        reg = '\d+'
        views = int("".join(re.findall(reg, views_str)))

        item['views'] = views
        item['comments'] = None
        item['likes'] = None
        item['forwards'] = None
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.item_path)
    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)