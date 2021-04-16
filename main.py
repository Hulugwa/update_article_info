import sys, judge_url,merge
from platforms import DefaultValues
import multiprocessing as mp
import os
import time
import pandas as pd
import traceback


__file_path = sys.argv[1]
if len(sys.argv) > 2:
    __field = sys.argv[2]
else:
    __field = '原文链接'

if __name__ == '__main__':
    # 删除已有的文件
    if os.path.exists(DefaultValues.result_path):
        os.remove(DefaultValues.result_path)
    if os.path.exists(DefaultValues.false_path):
        os.remove(DefaultValues.false_path)
    if os.path.exists(DefaultValues.rename_false):
        os.remove(DefaultValues.rename_false)
    if os.path.exists(DefaultValues.no_match_path):
        os.remove(DefaultValues.no_match_path)
    if os.path.exists(DefaultValues.merge_path):
        os.remove(DefaultValues.merge_path)

    time.sleep(3)

    # 开始解析excel并抓取
    pool = mp.Pool(10)
    datas = pd.read_excel(__file_path, index_col=0)
    print('抓取中......')
    for url in datas[__field]:
        pool.apply_async(judge_url.judge_url, args=(url,))
    pool.close()
    pool.join()
    print('首次抓取完成')
    print('----------------------------------')
    # with open(__file_path, 'r') as f:
    #     lines = f.readlines()
    #     print('抓取中.....')
    #     for line in lines:
    #         url = json.loads(line)['url']
    #         pool.apply_async(judge_url.judge_url, args=(url,))
    #     pool.close()
    #     pool.join()
    #     print('首次抓取完成')
    print("开始抓取失败链接")

    # 重新抓取一遍失败链接
    try:
        os.rename(DefaultValues.false_path, DefaultValues.rename_false)
        pool = mp.Pool(10)
        with open(DefaultValues.rename_false, 'r') as f:
            lines = f.readlines()
            for line in lines:
                pool.apply_async(judge_url.judge_url, args=(line, ))
            pool.close()
            pool.join()
    except:
        traceback.print_exc()
    print('失败链接抓取完成')
    print('----------------------------------')
    print('开始合并文件')

    # 合并文件
    merge.merge(__file_path, DefaultValues.result_path, __field)
    print('任务已完成，文件路径：' + DefaultValues.merge_path)
