from platforms import weibo, baijiahao, huafen, kuaizixun, \
    toutiao, wangyihao, yidianzixun, tieba, dayuhao, kandiankuaibao, qiehao, \
    zhihu, dongchedi, shoujisouhu, souhuhao, weibotoutiao, xinlangkandian, bilibili, \
    haokanshipin, qqkandian
import traceback
from platforms import DefaultValues, BaseFunctions


def judge_url(url):
    try:
        if 'weibo' in str(url):
            weibo.start(url)
        elif '360kuai' in url or 'm.news.so.com' in url:
            kuaizixun.start(url)
        elif 'www.163.com' in url or 'dy.163.com' in url or '3g.163.com' in url or 'dy.163.com' in url:
            wangyihao.wangyi(url)
        elif 'cn.club.vmall.com' in url or 'club.huawei.com' in url:
            huafen.vmall(url)
        elif 'baidu.com' in url and 'tieba' not in url:
            baijiahao.start(url)
        elif 'www.toutiao.com' in url or 'm.toutiaocdn.net' in url or 'toutiao.com' in url:
            toutiao.toutiao(url)
        elif 'yidianzixun' in url:
            yidianzixun.yidianzixun(url)
        elif 'tieba.baidu.com' in url:
            tieba.start(url)
        elif 'a.mp.uc.cn' in url or 'm.uczzd.cn' in url or 'iflow.uc.cn' in url:
            dayuhao.start(url)
        elif 'kuaibao.qq.com' in url:
            kandiankuaibao.start(url)
        elif 'new.qq.com' in url:
            qiehao.start(url)
        elif 'www.zhihu.com' in url:
            zhihu.start(url)
        elif 'dongchedi' in url:
            dongchedi.start(url)
        elif 'm.sohu.com' in url:
            shoujisouhu.start(url)
        elif 'www.sohu.com' in url or '3g.k.sohu' in url:
            souhuhao.start(url)
        elif 'ttarticle' in url:
            weibotoutiao.start(url)
        elif 'k.sina.com' in url:
            xinlangkandian.start(url)
        elif 'bilibili' in url:
            bilibili.start(url)
        elif 'haokan' in url:
            haokanshipin.start(url)
        elif 'post.mp.qq.com' in url:
            qqkandian.start(url)
        else:
            BaseFunctions.writeFalseUrl(url, DefaultValues.no_match_path)
    except:
        traceback.print_exc()