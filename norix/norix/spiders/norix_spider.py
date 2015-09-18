# -*- encoding: utf-8 -*-
import scrapy

import json
from scrapy.selector import Selector
from scrapy.crawler import Crawler
from scrapy.conf import settings
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from scrapy.exceptions import CloseSpider
from loginform import fill_login_form
from scrapy.http import Request
from norix.items import *
from twisted.internet import reactor
import re
from urlparse import urlparse
import hashlib
import bcrypt
import pymongo
from pymongo import ReturnDocument
import socket


class NorixSpider(CrawlSpider):

    name = 'norix'
    
    connection = pymongo.MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
    )
    db = connection[settings['MONGODB_DB']]

    def url_exists(self, hostname):

        try:
            self.logger.info(hostname)
            socket.gethostbyname(hostname)
            
            return True
        except socket.error as e:
            self.logger.info(e)
            return False 

    def get_dopostback_url(self, dopostback_url):            
        url = dopostback_url[0].split("'")
        url = url[1] 
        return url    

    def parse_start_url(self, response):    
        
        self.user = response.meta['user']
        self.club = response.meta['club']
        self.password = response.meta['password']
        self.logger.info('Logging in to:  %s', response.url)


        if self.url_exists(response.url.split('/')[2]):
            self.logger.info('User:  %s', response.meta['user'])
            self.logger.info('Password:  %s', response.meta['password'])
            args, url, method = fill_login_form(response.url, response.body, response.meta['user'], response.meta['password'])
            return FormRequest(url, method=method, formdata=args, callback=self.logged_in)
        else:
            # TODO: Nori returns 404 so let´s add that later
            raise CloseSpider('Url not found :-(')

    
    def delete_player_seminar_associations(self, user):
        self.logger.info('Deleting all seminar associations that contain: %s', user)
        user_seminar_db = self.db['seminar_seminar_has_users__user_user_has_seminars']
        player_seminar_db = self.db['player_seminars__seminar_players']
        seminars = user_seminar_db.find({'user_user_has_seminars': user['_id']})
        seminars = [d['seminar_seminar_has_users'] for d in seminars]        
        for seminar in seminars:
            self.logger.info('SEMINAR: %s', seminar)
        player_seminar_db.remove({'seminar_players': {'$in': seminars}})

    def add_user(self):            
            
            '''
            Login validation is missing, we need to write that very soon
            '''
            self.logger.info('Hi, I am in, what now... ')
            password = self.password.encode('utf-8')
            
            '''
            Changing the prefix since the node bcrypt package uses 2a, not 2b.
            '''
            hashed = bcrypt.hashpw(password, bcrypt.gensalt(10, prefix=b"2a"))            
            user_db = self.db['users']
            self.user_obj = user_db.find_one_and_update(
                {
                    'username': self.user,                    
                    'club': self.club,
                },

                {'$set': {
                    'username': self.user,                    
                    'club': self.club,                
                    'encryptedPassword': hashed,
                    }                
                },  
                return_document=ReturnDocument.AFTER,       
                upsert=True) 

            self.delete_player_seminar_associations(self.user_obj)

    def logged_in(self, response):
        self.logger.debug('Log message', extra={'response': response})
        requests = []
        club_seminar = {}
        club_seminar_list = []
        
        '''
        Check if login failed. Unstable, since I´m only checking for the error text.
        '''
        invalid_login = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_panelLogin"]/table/tr[4]/td/span[1]')        

        if not invalid_login:
            self.logger.info('Hi, I am in, lets continue...  %s' % response.url)
            '''
            Add the Nori user to our db
            '''            
            self.add_user()


            

            seminars = response.xpath('//table[@class="itemListTable"]/tr')
            items = []
            for i, seminar in enumerate(seminars):
                
                if i != 0:
                    seminar_item = SeminarItem()
                    seminar_item['sport_department'] = seminar.xpath('td[1]/text()').extract()[0].replace('\r\n','').strip()                
                    seminar_item['age_group'] = seminar.xpath('td[2]/a/text()').extract()[0].replace('\r\n','').strip()
                    seminar_item['seminar_name'] = seminar.xpath('td[3]/text()').extract()[0].replace('\r\n','').strip()
                    seminar_item['period'] = seminar.xpath('td[4]/text()').extract()[0].replace('\r\n','').strip()
                    seminar_item['players_count'] = seminar.xpath('td[5]/text()').extract()[0].replace('\r\n','').strip()
                    
                    '''
                    Hash a few names to create a seminar id.
                    '''
                    seminar_item['seminar_id'] = abs(hash(self.club+seminar_item['sport_department']+seminar_item['age_group']+seminar_item['seminar_name'])) % (10 ** 8)
                    
                    
                    '''
                    Get doPostBack id used by ASP when generating urls
                    '''
                    seminar_item['group_url'] = self.get_dopostback_url(seminar.xpath('td[2]/a/@href').extract())
                    
                    
                    yield seminar_item
                    
                    viewstate = response.xpath('//*[contains(@id, "__VIEWSTATE")]/@value').extract()
                    request = FormRequest.from_response(
                                    response,
                                    formname='aspnetform',
                                    formdata={
                                    '__EVENTTARGET': seminar_item['group_url'],
                                    '__EVENTARGUMENT': '',
                                    '__VIEWSTATE': viewstate[0],
                                    },
                                    dont_filter = True,
                                    dont_click = True,
                                    callback=self.parse_players,
                                    meta=seminar_item)
                    yield request     


        else:
            return          
            
    def parse_players(self, response):
        
        player_dict = {}
        player_list = []
        ready_data = []
        player_data = response.xpath('//table[@class="itemListTable"]/tr')
        items = []
        for i, player in enumerate(player_data):
            if i != 0:
                player_item = PlayerItem()
                player_item['ssn'] = player.xpath('td[1]/text()').extract()[0].replace('\r\n','').strip()
                player_item['player_name'] = player.xpath('td[2]/a/text()').extract()[0].replace('\r\n','').strip()
                player_item['email'] = player.xpath('td[3]/text()').extract()[0].replace('\r\n','').strip()
                player_item['phone'] = player.xpath('td[4]/text()').extract()[0].replace('\r\n','').strip()
                player_item['status'] = player.xpath('td[5]/text()').extract()[0].replace('\r\n','').strip()
                player_item['seminars'] = response.meta['seminar_id']
            
                
                yield player_item
                items.append(player_item)
        
        self.data = items
        
        

'''
# Started the crawl to player detail page but let´s do that later

for item in response.xpath('//*[contains(@id, "linkShowMember")]'):
    crazy_url = item.xpath('//a/@href').extract()
    for crazy in crazy_url:
        print(crazy)
    #player_url = crazy_url[0].split(',')[0].split('"')[1].replace('"','')
    #print(player_url)
#print(response.xpath('//*[contains(@id, "linkShowMember")]/a/@id').extract())
#player_urls = self.get_dopostback_url(response.xpath('//*[contains(@id, "linkShowMember")]/a/@href').extract())
#print(player_urls)

#for player in player_names:



return
'''