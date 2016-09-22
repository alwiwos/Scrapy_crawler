 #-*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
#from twisted.enterprise import adbapi
#import MySQLdb.cursors


#class SQLStorePipeline(object):
#    def __init__(self):
#        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='spider',
#                user='root', passwd='alwiwos', cursorclass=MySQLdb.cursors.DictCursor,
 #               charset='utf8', use_unicode=True)
 #   def process_item(self, item, spider):
 #       # run db query in thread pool
 #       self.dbpool.runInteraction(self._conditional_insert, item)
   #     return item

  #  def _conditional_insert(self, tx, item):
  ##      # create record if doesn't exist.
  #      # all this block run on it's own thread
   #     tx.execute(\
   #         "values (%s, %s, %s)",
   #         (item['question_title'][0],
    #         item['question_url'], '  '.join(item['Tag']))
    #        )



#class StackoverflowPipeline(object):

#    def __init__(self):
#        self.file = codecs.open('stackoverflow_data.json', mode='wb', encoding='utf-8')

 #   def process_item(self, item, spider):
 #       line = json.dumps(dict(item)) + '\n'
 #       self.file.write(line.decode("unicode_escape"))
 #       return item
 #   def spider_closed(self, spider):
 #       self.file.close()


#!/usr/bin/python
# -*- coding:utf-8 -*-

from StackOverflow import settings
import requests
import os


# 图片下载类
class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        if 'image_urls' in item:  # 如何‘图片地址’在项目中
            images = []  # 定义图片空集

 #           dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)
            dir_path = 'C:\Users\suxd1202\Desktop\image'
  #          if not os.path.exists(dir_path):
   #             os.makedirs(dir_path)
            for image_url in item['image_urls']:
                us = image_url.split('/')[3:]
                image_file_name = '_'.join(us)
                file_path = '%s/%s' % (dir_path, image_file_name)
                images.append(file_path)
                if os.path.exists(file_path):
                    continue

                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)

            item['images'] = images
        return item


