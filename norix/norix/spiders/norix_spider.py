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

    def __init__(self, **kw):
        super(NorixSpider, self).__init__(**kw)
        self.url = kw.get('url')
        self.allowed_domains = [kw.get('domain')]
        self.start_urls = [self.url + '/UsersLogin.aspx']
        self.export = []
        self.player_list = []        

        #self.link_extractor = LinkExtractor()
        #self.cookies_seen = set()


    #allowed_domains = ["armenningar.felog.is"]
    
    login_user = "levy"
    login_pass = "tkd"
    #find_group = '//a[contains(@id, "ctl00_ContentPlaceHolder1_repeaterUserAccess_")]'
    
    #find_player = '//table[contains(@class, "itemListTable")]/tbody/tr[contains(@class, "line")]/td[2]/a/text()'
    find_player = '//*[contains(@id, "linkShowMember")]/text()'
    #find_players = '//*[@id="ctl00_ContentPlaceHolder1_repeaterUserAccess_ctl02_LinkButton1"]'
    #find_players = '//body'

    def parse_start_url(self, response):
        args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_pass)
        return FormRequest(url, method=method, formdata=args, callback=self.logged_in)

    def logged_in(self, response):
        requests = []
        
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return
        # We've successfully authenticated, let's have some fun!
        else:
            self.log('Hi, I am in, let´s continue...  %s' % response.url)
            
            #groups = response.xpath('//a[contains(@id, "linkMembers")]/text()').extract()
            seminars = response.xpath('//table[@class="itemListTable"]/tr')
            
            #self.log('Seminars: %s' % seminars.extract())
            items = []
            row_data = []
            col_data = []
            data = []
            item_dict = {}


            data = []
            for i, seminar in enumerate(seminars):

                seminar_item = SeminarItem()                
                col_data = []
                item_dict = {}
                #item = SeminarItem()
                col = seminar.xpath('td/text()').extract()
                group_name = seminar.xpath('td/a/text()').extract()                
                group_url = seminar.xpath('td/a[contains(@id, "linkMembers")]/@href').extract()
                
                for url in group_url:
                    parsed_url = url.split("'")
                    group_url = parsed_url[1]

                #group_url = seminar.xpath('td').extract()
                col.extend(group_name)
                


                r = 0

                for r, s in enumerate(col):
                    stripped = s.strip()
                    if stripped:
                        col_data.append(s.strip())
                        
                        #print(str(r)+': '+s)
                for r, s in enumerate(col_data):
                    print(str(r)+': '+ s)

                if i != 0:

                    item_dict['id'] = i
                    item_dict['sport_department'] = col_data[0]
                    item_dict['name'] = col_data[1]
                    item_dict['group'] = col_data[4]
                    item_dict['period'] = col_data[2]
                    item_dict['players_count'] = col_data[3]
                    item_dict['group_url'] = group_url

                data.append(item_dict)

                #seminar = response.xpath('//*[contains(@id, "ctl00_ContentPlaceHolder1_repeaterUserAccess")]/text()').extract()
                #group_url = response.xpath('//a[contains(@id, "linkMembers")]/@href').extract()
                viewstate = response.xpath('//*[contains(@id, "__VIEWSTATE")]/@value').extract()
                #self.log('All groups: %s' % groups)
                #self.log(group_url)
                #self.log('Viewstate: %s' % viewstate[0])
                request = FormRequest.from_response(
                                response,
                                formname='aspnetform',                            
                                #method='post',
                                #url='https://umfg.felog.is/MyPage.aspx',                                
                                formdata={
                                '__EVENTTARGET': group_url,
                                '__EVENTARGUMENT': '',
                                #'__VIEWSTATE': viewstate[0],
                                },
                                dont_filter = True,
                                callback=self.parse_players)
                yield request                   
                
            self.export = json.dumps(data, indent=4)
            

            #self.log('Column values: %s' % data)                    
                
                #item['name'] = group.xpath('//td['+i+'])

          
            #request = Request(group_url[0], callback = self.parse_players)
            
    def parse_players(self, response):
        #self.log('Lets see all players! %s' % response.body)
        player_item = PlayerItem()
        
        player_names = response.xpath(self.find_player)
        
        for name in player_names:
            player_item['name'] = name.extract()
            player_dict['name'] = name.extract()

            self.player_list.append(player_dict)

            yield player_item
