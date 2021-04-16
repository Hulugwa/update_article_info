# 以下操作均在dev服务器

# 项目路径
/home/report/gen_report/update_article_info

# 执行文件路径
/home/report/gen_report/update_article_info/main.py

# 执行方法
## 1. 激活python环境
source /home/report/gen_report/update_article_info/python3/bin/activate
## 2. 运行main文件
python /home/report/gen_report/update_article_info/main.py /home/report/f.xlsx 原文链接
## 3. 参数说明
第二步中，'/home/report/f.xlsx' 为源excel文件路径。'原文链接'为链接字段名称，可以省略，默认为'原文链接'，如果字段有变更需要传入新的字段名称

# 结果文件说明
## 文件路径
/home/report/results.xlsx，文件路径和文件名固定
## 文件新增字段
url -- 链接，与'原文链接相同'，如果没有即表示没有抓取到    
comments -- 更新后的评论量，如果没有即表示没有抓取到或者不存在此字段    
forwards -- 更新后的转发量，如果没有即表示没有抓取到或者不存在此字段    
likes -- 更新后的点赞量，如果没有即表示没有抓取到或者不存在此字段   
views -- 跟新后的阅读量，如果没有即表示没有抓取到或者不存在此字段   
