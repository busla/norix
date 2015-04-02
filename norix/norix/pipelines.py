# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from norix.items import *
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class PlayersPipeline(object):

    def __init__(self):
        connection = pymongo.Connection(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db['players']
        

    def process_item(self, item, spider):
        if not isinstance(item,PlayerItem):
            return item # return the item to let other pipeline to handle it
        self.collection.update({'ssn': item['ssn']}, dict(item), upsert=True)

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            #self.collection.insert(dict(item))
            #self.collection.findAndModify(dict(item), {'upsert':'true'});
            log.msg("Player added to collection",
                    level=log.DEBUG, spider=spider)
        return item

class SeminarPipeline(object):

    def __init__(self):
        connection = pymongo.Connection(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db['seminars']
        

    def process_item(self, item, spider):
        if not isinstance(item,SeminarItem):
            return item # return the item to let other pipeline to handle it
        self.collection.update({'id': item['id']}, dict(item), upsert=True)

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            #self.collection.insert(dict(item))
            #self.collection.findAndModify(dict(item), {'upsert':'true'});
            log.msg("Seminar added to collection",
                    level=log.DEBUG, spider=spider)
        return item