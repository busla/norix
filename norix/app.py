# -*- coding: utf-8 -*-
#!flask/bin/python
#from norix.crawler import CrawlerWorker
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, abort, Api, Resource, fields, marshal, marshal_with
from collections import OrderedDict




from flask import json
from flask import Flask, make_response, Response
from norix.spiders.norix_spider import NorixSpider
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from flask import Flask, jsonify
#from flask.ext.pymongo import PyMongo
from bson import json_util
from scrapy.conf import settings as scrapy_settings
import pymongo

#from flask.ext.restful import reqparse
#from mongokit import Connection, Document
app = Flask(__name__)
api = restful.Api(app)


#mongo = PyMongo(app)

parser = reqparse.RequestParser()
parser.add_argument('club', type=str, required=True, help='Why is this empty?')
parser.add_argument('username', type=str, required=True, help='Why is this empty?')
parser.add_argument('password', type=str, required=True, help='Why is this empty?')


def toJson(data):
    """Convert Mongo object(s) to JSON"""
    return json.dumps(data, default=json_util.default)


class Index(restful.Resource):
    def get(self):
        return {'Welcome': 'Yei!'}

class Players(restful.Resource):
    #@marshal_with(resource_fields, envelope='resource')
    #self.collection = db['players']

    def get(self):
        connection = pymongo.Connection(
            scrapy_settings['MONGODB_SERVER'],
            scrapy_settings['MONGODB_PORT']
        )
        db = connection[scrapy_settings['MONGODB_DB']]
        args = parser.parse_args()
        '''
        We run the spider using the GET parameters.
        '''
        arg_list = []
        arg_list.extend([args['club'], args['username'], args['password']])
        login_data = ','.join(arg_list)
        
        '''
        Let´s instantiate the spider to get all class properties
        '''
        spider = NorixSpider(arguments=login_data)
        collection_name = spider.subdomain+'_'+spider.user+'_players'
        print(db.collection_names())
        print(collection_name)
        '''
        Check if the player collection exists
        '''
        if collection_name in db.collection_names():
            print('Collection exists!')
            pass

        else:            

            '''
            If player collection does not exist, run the spider on [club].felog.is
            which saves the results to db.
            '''        

            settings = get_project_settings()
            crawler = Crawler(settings)
            crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            crawler.configure()
            crawler.crawl(spider)
            crawler.start()
            log.start()
            reactor.run(installSignalHandlers=0) # Prevent: exceptions.ValueError: signal only works in main thread
            return {'Message': 'Scraping Nori and saving to DB. Refresh after a couple of seconds to get some goodies!'}
        
        '''
        Get all players from db.
        '''            
        player_list = list(db[collection_name].find())
        #return self.output_json(player_list, 200)
        #return json.dumps(marshal(player_list, resource_fields))
        
        response = make_response(Response(json.dumps({'data': player_list}, default=json_util.default),
                mimetype='application/json'))
        response.headers['Access-Control-Allow-Origin'] = "*"
        return response
        
        '''
        json_results = []
        for player in player_list:
          json_results.append(player)
        return toJson(json_results)
        #return json.dumps(marshal(json_results, resource_fields))
        '''
    
api.add_resource(Players, '/players')
api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0'))

