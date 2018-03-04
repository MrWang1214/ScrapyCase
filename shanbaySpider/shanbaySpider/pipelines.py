# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import pymysql
import time
from twisted.enterprise import adbapi
from scrapy.conf import settings


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('data_shanbay.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))
        return item


class MysqlWithJsonPipeline(object):
    def __init__(self):
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        #**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    def insert(self, item):
        sql = "INSERT INTO daily_translation (daily_translation_title, daily_translation_author, daily_translation_date) VALUES(%s,%s,%s)"
        #调用插入的方法
        self.dbpool.runInteraction(self._conditional_insert, sql, item)

    def _conditional_insert(self, tx, sql, item):
        params = (item["title"], item['author'], item['topic_post_time'])
        tx.execute(sql, params)
    
    def process_item(self, item, spider):
        # 插入数据库
        self.insert(item)
        return item