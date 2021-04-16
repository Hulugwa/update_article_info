from platforms import BaseFunctions, DefaultValues
import re
import json


def start(url):
    try:
        item = {}
        response = BaseFunctions.requests().get(url, verify=False, proxies=DefaultValues.proxies).content.decode('unicode-escape')

        reg = r'window.__PRELOADED_STATE__\s*=\s*({.*})\s*;'
        data = json.loads("".join(re.findall(reg, str(response))))

        item['views'] = int(data['curVideoMeta']['playcnt'])
        item['comments'] = int(data['curVideoMeta']['fmcomment_num'])
        item['likes'] = int(data['curVideoMeta']['fmlike_num'])
        item['forwards'] = None
        item['url'] = url

        BaseFunctions.writeFile(item, DefaultValues.result_path)

    except:
        BaseFunctions.writeFalseUrl(url, DefaultValues.false_path)