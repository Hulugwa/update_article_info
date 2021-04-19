from update_article_info.utils import BaseFunctions, DefaultValues
import re
import json
from lxml import etree

headers = {
    'Cookie': 'BIDUPSID=1383147E2319AEE5CA75ECC35297D2C8; PSTM=1613722260; BAIDUID=1383147E2319AEE5E882518D590F0414:FG=1; HOSUPPORT=1; HOSUPPORT_BFESS=1; UBI=fi_PncwhpxZ%7ETaKAQyE5Vo7xvY9oHZxW5nShNvK2OOSVm8gJaAmPbLDoJQ-c7G-pRxA3BYillxgdPMeyuNgy3KfrgpsKMhnG9dTSr1DnmosahktIQuzgJDSa5TdeR97iYOwl6FrDzm6nJM1YzohRKqOv1Fspw__; UBI_BFESS=fi_PncwhpxZ%7ETaKAQyE5Vo7xvY9oHZxW5nShNvK2OOSVm8gJaAmPbLDoJQ-c7G-pRxA3BYillxgdPMeyuNgy3KfrgpsKMhnG9dTSr1DnmosahktIQuzgJDSa5TdeR97iYOwl6FrDzm6nJM1YzohRKqOv1Fspw__; USERNAMETYPE=2; SAVEUSERID=0ef05a85ddd3b054cd3703ee0c1c40f462016b; HISTORY=21f6ff8371d517b0c91acde09285ec7cbf2d5f32a5005b; USERNAMETYPE_BFESS=2; SAVEUSERID_BFESS=0ef05a85ddd3b054cd3703ee0c1c40f462016b; HISTORY_BFESS=21f6ff8371d517b0c91acde09285ec7cbf2d5f32a5005b; MCITY=-340%3A; H_WISE_SIDS=110085_127969_131423_144966_154619_156287_156928_160878_162898_163568_165135_166148_166185_166692_167085_167112_167300_168033_168204_168494_168543_168626_168747_168763_168768_169066_169156_169308_169405_169694_169788_169883_170292_170459_170468_170578_170580_170583_170590_170745_170917_170959; __yjs_duid=1_b5c6c67e78b1a567d768ff3e08eb04f41616555417619; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=33820_33749_33273_33714_26350_22160; delPer=0; PSINO=6; BAIDUID_BFESS=1383147E2319AEE5E882518D590F0414:FG=1; ZD_ENTRY=baidu; Hmery-Time=1973883774; BA_HECTOR=0k210k248k208g0k781g79umj0q; STOKEN=3ffe50101870fbda17455a000a65a7901ee925a9f7f7ef1a4df98879ce04e240; BDUSS=W1rd21zOVBabS1YakRRU3JzSTUxOEkzOS1zZUIwUFRXZnJ1SVVzQi1GM2VoNXhnSVFBQUFBJCQAAAAAAAAAAAEAAACTdUFHzOzQq8XLtuDArdauyfEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN76dGDe-nRgR; PTOKEN=8ac6885eb76c4bcb7984bf9ae9c5d2ba; logTraceID=677e8b3ebb7754847e13e16cf20b2ba10ad8e318e8f06270ed; BDUSS_BFESS=W1rd21zOVBabS1YakRRU3JzSTUxOEkzOS1zZUIwUFRXZnJ1SVVzQi1GM2VoNXhnSVFBQUFBJCQAAAAAAAAAAAEAAACTdUFHzOzQq8XLtuDArdauyfEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN76dGDe-nRgR; STOKEN_BFESS=3ffe50101870fbda17455a000a65a7901ee925a9f7f7ef1a4df98879ce04e240; PTOKEN_BFESS=8ac6885eb76c4bcb7984bf9ae9c5d2ba; pplogid=8671PgxTFFKtqsEqK1xgF2FniI0UpEodpt4hnjblaFkgm%2BwbfNHShzQBqbDNmyTSODk3vvG5zhvOXXIkgWRslW63GwF1Zp44Da33wfiHqmdLUM8%3D; pplogid_BFESS=8671PgxTFFKtqsEqK1xgF2FniI0UpEodpt4hnjblaFkgm%2BwbfNHShzQBqbDNmyTSODk3vvG5zhvOXXIkgWRslW63GwF1Zp44Da33wfiHqmdLUM8%3D'
}


def get_id(url):
    try:
        response = BaseFunctions.requests().get(url, verify=False, timeout=DefaultValues.timeout,
                                                proxies=DefaultValues.proxies)
        reg = r'window.jsonData\s*=\s*({.*?});'
        data = json.loads("".join(re.findall(reg, response.text)))

        feed_id = data['bsData']['superlanding'][0]['itemData']['notice']['id']
        thread_id = data['bsData']['comment']['tid']
        uk = data['bsData']['profitLog']['contentAccId']

        return (feed_id, thread_id, uk)

    except:
        pass


def start(url):
    try:
        if 'baijiahao' in url or 'news_' in url:
            baijiahao(url)
        elif 'nid=dt_' in url:
            newspage_dt(url)
        elif 'knowpage' in url:
            knowpage(url)
        else:
            pass
    except:
        pass


def baijiahao(url):
    try:
        item = {}
        source_url = 'https://mbd.baidu.com/webpage?type=homepage&action=interact&format=jsonp&params=[{"feed_id":"%s","thread_id":"%s","dynamic_type":"2","dynamic_sub_type":"2001"}]&uk=%s'
        ids = get_id(url)
        request_url = source_url % (ids[0], ids[1], ids[2])

        response = BaseFunctions.requests().get(request_url, verify=False, proxies=DefaultValues.proxies,
                                                headers=headers)
        json_str = "".join(re.findall(r'callback\((.*)\)', response.text))
        data = json.loads(json_str)

        item['likes'] = int(data['data']['user_list']['_2001_']['praise_num'])
        item['comments'] = int(data['data']['user_list']['_2001_']['comment_num'])
        item['views'] = int(data['data']['user_list']['_2001_']['read_num'])
        item['forwards'] = None
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)


def newspage_dt(url):
    try:
        item = {}

        response = BaseFunctions.requests().get(url, verify=False, proxies=DefaultValues.proxies)
        reg = r'window.jsonData\s*=\s*({.*?});'
        data = json.loads("".join(re.findall(reg, response.text)))

        item['views'] = int(data['data']['pageInfo']['interaction_data']['readNum']['count'])
        item['likes'] = int(data['data']['pageInfo']['interaction_data']['praise']['praise_num'])
        item['forwards'] = int(data['data']['pageInfo']['interaction_data']['forwardNum'])
        item['comments'] = int(data['data']['pageInfo']['interaction_data']['commentNum'])
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)


def knowpage(url):
    source_url = 'https://mbd.baidu.com/knowpage/api/getdynamicinfo?crid={crid}&qid={qid}'
    try:
        item = {}
        reg = 'qid=(.*)'
        qid = "".join(re.findall(reg, url))

        response = BaseFunctions.requests().get(url, verify=False, proxies=DefaultValues.proxies)
        html = etree.HTML(response.text)
        crid = "".join(html.xpath("//li[@class='reply-item tpl-reply-item'][1]/@data-rid"))

        request_url = source_url.format(crid=crid, qid=qid)
        response1 = BaseFunctions.requests().get(request_url, verify=False, proxies=DefaultValues.proxies)
        data = json.loads(response1.text)

        likes = int(data['data']['replies']['list'][0]['thumbUp'])
        comments = int(data['data']['replies']['list'][0]['commentCount'])

        item['comments'] = comments
        item['likes'] = likes
        item['views'] = None
        item['forwards'] = None
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.item_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)
