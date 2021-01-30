# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JdBookPipeline:
    def __init__(self):
        self.number = 0
        client = MongoClient(host='127.0.0.1', port=27017)
        self.collection = client["spider"]["books"]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        self.number += 1
        print('第', self.number, '本书存入成功')
        return item
