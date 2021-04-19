import os
import sys
cur_path=os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path+"/..")

from update_article_info.funcs import judge_url, merge
from update_article_info.utils import DefaultValues
import multiprocessing as mp
import time
import pandas as pd
import traceback
import fire


def update(input_path, output_path, field=DefaultValues.field):
    # 删除已有的文件
    if os.path.exists(DefaultValues.false_path):
        os.remove(DefaultValues.false_path)
    if os.path.exists(DefaultValues.item_path):
        os.remove(DefaultValues.item_path)

    time.sleep(3)

    # 开始解析excel并抓取
    pool = mp.Pool(10)
    datas = pd.read_excel(input_path, index_col=0)
    print('抓取中......')
    try:
        for url in datas[field]:
            pool.apply_async(judge_url.judge_url, args=(url,))
        pool.close()
        pool.join()
        print('首次抓取完成')
    except:
        traceback.print_exc()
    print('----------------------------------')

    print("开始抓取失败链接")

    # 重新抓取一遍失败链接
    if os.path.exists(DefaultValues.false_path):
        try:
            pool = mp.Pool(10)
            with open(DefaultValues.false_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    pool.apply_async(judge_url.judge_url, args=(line,))
                pool.close()
                pool.join()
        except:
            traceback.print_exc()
    print('失败链接抓取完成')
    print('----------------------------------')
    print('开始合并文件')

    try:
        # 合并文件
        merge.merge(input_path, output_path, DefaultValues.item_path, field)
        print('任务已完成，文件路径：' + output_path)
    except:
        traceback.print_exc()

    # 删除中间文件
    if os.path.exists(DefaultValues.false_path):
        os.remove(DefaultValues.false_path)
    if os.path.exists(DefaultValues.item_path):
        os.remove(DefaultValues.item_path)


def commandline():
    fire.Fire(update)


if __name__ == '__main__':
    commandline()