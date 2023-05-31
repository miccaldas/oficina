# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):
    collection_name = "questions"

    def __init__(self):
        connection = pymongo.MongoClient("localhost", 27017)
        self.db = connection["stackoverflow"]
        self.collection = "questions"

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
