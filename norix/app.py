# -*- coding: utf-8 -*-
#!flask/bin/python
#from norix.crawler import CrawlerWorker
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, abort, Api, Resource, fields, marshal, marshal_with
from collections import OrderedDict
import requests
import json
from urlparse import urljoin


from flask import json
from flask import Flask, make_response, Response
from norix.spiders.norix_spider import NorixSpider
from twisted.internet import reactor
from scrapy.crawler import Crawler, Settings
from scrapy.crawler import CrawlerProcess
from scrapy import signals
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
parser.add_argument('user', type=str, required=True, help='Why is this empty?')
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
        
        collection_name = args['club']+'_'+args['user']+'_players'
        print(db.collection_names())
        print(collection_name)
        '''
        Check if the player collection exists
        '''
        if collection_name in db.collection_names():
            print('Collection exists!')
            pass


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

class Scrape(restful.Resource):
    #@marshal_with(resource_fields, envelope='resource')
    #self.collection = db['players']

    def get(self):
        args = parser.parse_args()
        '''
        We run the spider using the GET parameters.
        '''
        nori_url = urljoin('http://'+args['club']+'.felog.is','UsersLogin.aspx')
        scrapy_url = urljoin('http://127.0.0.1:9080','crawl.json')    
        payload = {"spider_name":"norix", "request": {"url": nori_url, "meta": {"user": args['user'], "password": args['password']}}}
        
        r = requests.post(scrapy_url, data=json.dumps(payload))
        print(r)
        '''
        Let´s instantiate the spider to get all class properties
        '''
        #spider = NorixSpider(arguments=login_data)

        '''
        If player collection does not exist, run the spider on [club].felog.is
        which saves the results to db.
        '''        
        '''                
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        spider = NorixSpider(arguments=login_data)
        settings = get_project_settings()
        runner = CrawlerRunner(settings)        
        d = runner.crawl(spider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run() # the script will block here until the crawling is finished
        '''        

        '''
        process = CrawlerProcess(get_project_settings())
        # 'followall' is the name of one of the spiders of the project.
        process.crawl('norix', arguments=login_data)
        process.start() # the script will block here until the crawling is finished                
        '''
  
        '''
        #spider = NorixSpider(arguments=login_data)
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start()
        reactor.run(installSignalHandlers=0) # Prevent: exceptions.ValueError: signal only works in main thread
        '''
        #return self.output_json(player_list, 200)
        #return json.dumps(marshal(player_list, resource_fields))
        return {'Message': 'Done scraping!'}

        
        '''
        json_results = []
        for player in player_list:
          json_results.append(player)
        return toJson(json_results)
        #return json.dumps(marshal(json_results, resource_fields))
        '''

api.add_resource(Players, '/players')
api.add_resource(Scrape, '/scrape')
api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', debug=True))

