# -*- encoding: utf-8 -*-
import scrapy

import json
from scrapy.selector import Selector
from scrapy.crawler import Crawler
#from scrapy import log, signals
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from loginform import fill_login_form
#from scrapy.contrib.djangoitem import DjangoItem
from scrapy.http import Request
from norix.items import *
from twisted.internet import reactor
import re
from urlparse import urlparse

class NorixSpider(CrawlSpider):

    name = 'norix'


    '''
    def __init__(self, arguments=None, *args, **kwargs):
        super(NorixSpider, self).__init__(*args, **kwargs)
        #self.url = kw.get('url')

        self.arguments = arguments.split(',')
        self.subdomain = self.arguments[0]
        self.domain = self.arguments[0].strip()+'.felog'+'.is'
        self.allowed_domains = [self.domain]
        self.start_urls = ['http://'+self.domain+'/UsersLogin.aspx']
        self.user = self.arguments[1].strip()
        self.password = self.arguments[2].strip()
        self.data = []

    '''
    def get_dopostback_url(self, dopostback_url):            
        url = dopostback_url[0].split("'")
        url = url[1] 
        return url    

    def parse_start_url(self, response):
        self.logger.info('Logging in to:  %s', response.url)
        self.logger.info('User:  %s', response.meta['user'])
        self.logger.info('Password:  %s', response.meta['password'])
        args, url, method = fill_login_form(response.url, response.body, response.meta['user'], response.meta['password'])
        return FormRequest(url, method=method, formdata=args, callback=self.logged_in)




    def logged_in(self, response):
        
        requests = []
        club_seminar = {}
        club_seminar_list = []
        
        '''
        Check if login failed. Unstable, since I´m only checking for the error text.
        '''
        invalid_login = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_panelLogin"]/table/tr[4]/td/span[1]')
        #print(invalid_login.extract())

        if not invalid_login:
            '''
            Login validation is missing, we need to write that very soon
            '''
            print(response.body)
            #print(response.body)
            self.logger.info('Hi, I am in, what now... ')
            #self.log('Hi, I am in, let´s continue...  %s' % response.url)
            
            #groups = response.xpath('//a[contains(@id, "linkMembers")]/text()').extract()
            seminars = response.xpath('//table[@class="itemListTable"]/tr')
            items = []
            for i, seminar in enumerate(seminars):
                
                if i != 0:
                    seminar_item = SeminarItem()
                    seminar_item['sport_department'] = seminar.xpath('td[1]/text()').extract()[0].replace('\r\n','').strip()                
                    seminar_item['age_group'] = seminar.xpath('td[2]/a/text()').extract()[0].replace('\r\n','').strip()
                    seminar_item['seminar'] = seminar.xpath('td[3]/text()').extract()[0].replace('\r\n','').strip()
                    seminar_item['period'] = seminar.xpath('td[4]/text()').extract()[0].replace('\r\n','').strip()
                    seminar_item['players_count'] = seminar.xpath('td[5]/text()').extract()[0].replace('\r\n','').strip()
                    seminar_item['id'] = seminar_item['sport_department'].lower()+str(i)+seminar_item['seminar'].lower()+seminar_item['period'].replace('.','').replace('-','').replace(' ','')
                    
                    # Get doPostBack id used by ASP when generating urls                 
                    seminar_item['group_url'] = self.get_dopostback_url(seminar.xpath('td[2]/a/@href').extract())
                    
                    
                    yield seminar_item
                    
                    viewstate = response.xpath('//*[contains(@id, "__VIEWSTATE")]/@value').extract()
                    request = FormRequest.from_response(
                                    response,
                                    formname='aspnetform',                            
                                    #method='post',
                                    #url='https://umfg.felog.is/MyPage.aspx',                                
                                    formdata={
                                    '__EVENTTARGET': seminar_item['group_url'],
                                    '__EVENTARGUMENT': '',
                                    '__VIEWSTATE': viewstate[0],
                                    },
                                    dont_filter = True,
                                    callback=self.parse_players,
                                    meta=seminar_item)
                    yield request     


        else:
            return              
                
            #self.export = json.dumps(data, indent=4)
            

            #self.log('Column values: %s' % data)                    
                
                #item['name'] = group.xpath('//td['+i+'])

          
            #request = Request(group_url[0], callback = self.parse_players)
            
    def parse_players(self, response):
        #self.log('Lets see all players! %s' % response.body)
        
        player_dict = {}
        player_list = []
        ready_data = []

        #players = response.xpath('//*[contains(@id, "linkShowMember")]/text()').extract()
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
                player_item['seminars'] = response.meta['id']
                
                # Get doPostBack id used by ASP when generating urls                 
                #club_sport['group_url'] = self.get_dopostback_url(seminar.xpath('td[2]/a/@href').extract())
                #player_list.append(player_item)
                
                yield player_item
                items.append(player_item)
        #print(items)
        self.data = items
        #return items
        




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