import requests
requests.packages.urllib3.disable_warnings()
from requests.adapters import HTTPAdapter
import json


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
    # read_path = '/Users/petezhang/Desktop/source-all.json'
    # result_path = 'data/news.json'
    # false_path = 'data/false.json'
    # rename_false = 'data/first_false.json'
    # no_match_path = 'data/no_match.json'
    # merge_path = 'data/results.xlsx'

    # dev
    result_path = '/home/report/gen_report/update_article_info/data/news.json'
    false_path = '/home/report/gen_report/update_article_info/data/false.json'
    rename_false = '/home/report/gen_report/update_article_info/data/first_false.json'
    no_match_path = '/home/report/gen_report/update_article_info/data/no_match.json'
    merge_path = '/home/report/results.xlsx'