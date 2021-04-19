import requests
requests.packages.urllib3.disable_warnings()
from requests.adapters import HTTPAdapter
import json
import os


class BaseFunctions:

    @classmethod
    def requests(cls):
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=3))
        session.mount('https://', HTTPAdapter(max_retries=3))

        return session

    @classmethod
    def writeFile(cls, item, path):
        with open(f'{path}', 'a') as f:
            f.write(json.dumps(item))
            f.write('\n')


    @classmethod
    def writeFalseUrl(cls, url, path):
        with open(f'{path}', 'a') as f:
            f.write(url)
            f.write('\n')

class DefaultValues:

    proxies = {
        'http': 'http://192.168.1.222:58189',
        'https': 'http://192.168.1.222:58189',
    }

    timeout = 5

    # 本机
    path = os.path.expandvars('$HOME')
    item_path = f'{path}/news.json'
    false_path = f'{path}/false.json'
    field = '原文链接'