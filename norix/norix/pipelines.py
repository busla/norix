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
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]

    def process_item(self, item, spider):
        if not isinstance(item,PlayerItem):
            return item # return the item to let other pipeline to handle it
        db = self.db
        collection = db['players']

        collection.update(
            {
                'ssn': item['ssn']
            },
            {
                'ssn': item['ssn'],
                'player_name': item['player_name'],
                'email': item['email'],
                'phone': item['phone'],
                'status': item['status']            
            }, 
            upsert=True)

        collection = db['player_seminars__seminar_players']        
        collection.update(
            {
                'seminar_players': item['seminars'],
                'player_seminars': item['ssn']
            },
            {
                'seminar_players': item['seminars'],
                'player_seminars': item['ssn']
            },             
            upsert=True)        

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
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        
        

    def process_item(self, item, spider):
        if not isinstance(item,SeminarItem):
            return item # return the item to let other pipeline to handle it
        db = self.db
        collection = db['seminars']
        collection.update({'seminar_id': item['seminar_id']}, dict(item), upsert=True)

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