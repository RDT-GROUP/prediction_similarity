# 外源性物质体内代谢数据收集及预测网站

框架依赖：
- python 3.6.5
- Django 3.2.5

其他依赖：
- rdkit
- pandas
- argparse
- pymysql
- json
- xlrd

## media 
- 用于保存固定的图片信息；例如：1.dot.png
- 用于自动生成的图片数据信息。

## prediction_similarity
- 用于域名解析+环境配置

## web
- views：用于前端数据交互
- db：用于数据库管理
- sim：用于预测算法
