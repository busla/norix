# -*- encoding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.http import HtmlResponse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from loginform import fill_login_form
from scrapy.contrib.djangoitem import DjangoItem
from scrapy.http import Request
from norix.items import *
from twisted.internet import reactor
import re
from urlparse import urlparse

class NorixSpider(CrawlSpider):

    name = 'norix'
    
    '''
    clubs = {
        'armann': {
            'user': 'levy',
            'password': 'tkd',
        },
        'umfg': {
            'user': 'levy',
            'password': '190881',
        },
    }
    '''

    def __init__(self, arguments=None, *args, **kwargs):
        super(NorixSpider, self).__init__(*args, **kwargs)
        #self.url = kw.get('url')

        self.arguments = arguments.split(',')
        domain = self.arguments[0].strip()+'.felog'+'.is'
        self.allowed_domains = [domain]
        self.start_urls = ['http://'+domain+'/UsersLogin.aspx']
        self.user = self.arguments[1].strip()
        self.password = self.arguments[2].strip()

   
    def get_dopostback_url(self, dopostback_url):            
        url = dopostback_url[0].split("'")
        url = url[1] 
        return url    

    def parse_start_url(self, response):
        
        args, url, method = fill_login_form(response.url, response.body, self.user, self.password)
        return FormRequest(url, method=method, formdata=args, callback=self.logged_in)




    def logged_in(self, response):
        requests = []
        club_seminar = {}
        club_seminar_list = []

        '''
        Login validation is missing, we need to write that very soon
        '''
        print(response.body)
        self.log('Hi, I am in, let´s continue...  %s' % response.url)
        
        #groups = response.xpath('//a[contains(@id, "linkMembers")]/text()').extract()
        seminars = response.xpath('//table[@class="itemListTable"]/tr')

        for i, seminar in enumerate(seminars):
            
            if i != 0:
                seminar_item = SeminarItem()
                seminar_item['sport_department'] = seminar.xpath('td[1]/text()').extract()[0].replace('\r\n','').strip()
                seminar_item['age_group'] = seminar.xpath('td[2]/a/text()').extract()[0].replace('\r\n','').strip()
                seminar_item['seminar'] = seminar.xpath('td[3]/text()').extract()[0].replace('\r\n','').strip()
                seminar_item['period'] = seminar.xpath('td[4]/text()').extract()[0].replace('\r\n','').strip()
                seminar_item['players_count'] = seminar.xpath('td[5]/text()').extract()[0].replace('\r\n','').strip()
                
                # Get doPostBack id used by ASP when generating urls                 
                seminar_item['group_url'] = self.get_dopostback_url(seminar.xpath('td[2]/a/@href').extract())
                print(seminar_item)
      
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

        for i, player in enumerate(player_data):
            if i != 0:
                player_item = PlayerItem()
                player_item['ssn'] = player.xpath('td[1]/text()').extract()[0].replace('\r\n','').strip()
                player_item['player_name'] = player.xpath('td[2]/a/text()').extract()[0].replace('\r\n','').strip()
                player_item['email'] = player.xpath('td[3]/text()').extract()[0].replace('\r\n','').strip()
                player_item['phone'] = player.xpath('td[4]/text()').extract()[0].replace('\r\n','').strip()
                player_item['status'] = player.xpath('td[5]/text()').extract()[0].replace('\r\n','').strip()
                
                # Get doPostBack id used by ASP when generating urls                 
                #club_sport['group_url'] = self.get_dopostback_url(seminar.xpath('td[2]/a/@href').extract())
                #player_list.append(player_item)
                print(player_item)

        return player_item
        




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