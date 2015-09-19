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
import logging
import json
from bson import BSON
from bson import json_util

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
        players = db['players']
        player_seminars = db['player_seminars__seminar_players']

        players.update(
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
        
        
        player_seminars.insert_one(
            {
                'seminar_players': item['seminars'],
                'player_seminars': item['ssn']
            })        

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            #self.collection.insert(dict(item))
            #self.collection.findAndModify(dict(item), {'upsert':'true'});
            spider.logger.info("Player %s added to collection", item['player_name'])

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
        seminar = db['seminars']
        #user_db = db['users']
        user_seminars = db['seminar_seminar_has_users__user_user_has_seminars']        

        seminar.update({'seminar_id': item['seminar_id']}, dict(item), upsert=True)
        
        #find_user = user_db.find({'username': spider.user, 'club': spider.club})
        
        #spider.logger.info(spider.user_obj['_id'])
        
        user_seminars.update({
            'user_user_has_seminars': spider.user_obj['_id'],            
            'seminar_seminar_has_users': item['seminar_id']
            },
            {
            'user_user_has_seminars': spider.user_obj['_id'],
            'seminar_seminar_has_users': item['seminar_id']
            },                        
            upsert=True) 
        
        
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            spider.logger.info("Seminar %s added to collection", item['seminar_name'])
            
        return item