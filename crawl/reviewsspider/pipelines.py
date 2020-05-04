# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import jieba
from sklearn.externals import joblib

model = joblib.load('../../model/model.normal')


class ReviewsspiderPipeline(object):

    def open_spider(self, spider):
        self.db = pymysql.connect(host="localhost", user="root",
                                  passwd="wstc9093", db="comment")
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        emotion = model.predict([' '.join(list(jieba.cut(item['review'])))])

        if int(emotion[0]) == 1:
            item['emotion'] = '正面'
        elif int(emotion[0]) == 0:
            item['emotion'] = '负面'

        sql = '''INSERT INTO comments(date, rating, title, review, emotion) VALUES(%s, %s, %s, %s, %s)'''
        value = (item['date'], item['rating'], item['title'],
                 item['review'], item['emotion'])
        # print(f"value: {value}")
        try:
            self.cursor.execute(sql, value)
            self.db.commit()
        except Exception as e:
            print(f"error_reason: {e}")
        return

    def close_spider(self, spider):
        self.db.close()
