import pandas as pd
from pandas import ExcelWriter
import traceback


def merge(input_path, output_path, item_path, field):
    try:
        json_data = pd.read_json(item_path, lines=True)
        source_excel = pd.read_excel(input_path, index_col=0)

        results = source_excel.merge(json_data, left_on=field, right_on='url', how='left')

        # 替换值
        results = results.fillna({'url': '?', 'comments': '-', 'forwards': '-', 'likes': '-', 'views': '-'})
        results.loc[results['url'] == '?', 'comments'] = '?'
        results.loc[results['url'] == '?', 'forwards'] = '?'
        results.loc[results['url'] == '?', 'likes'] = '?'
        results.loc[results['url'] == '?', 'views'] = '?'

        # 删除列
        results = results.drop('url', 1)

        # 重命名列
        results = results.rename(columns={'comments': '新评论量', 'forwards': '新转发量', 'likes': '新点赞量', 'views': '新阅读量'})

        with ExcelWriter(output_path) as writer:
            results.to_excel(writer)
    except:
        traceback.print_exc()