# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
#from scrapy.contrib.djangoitem import DjangoItem
from scrapy.item import Field


class SeminarItem(scrapy.Item):
    # define the fields for your item here like:
    seminar_id = scrapy.Field()
    sport_department = scrapy.Field()
    age_group = scrapy.Field()
    seminar_name = scrapy.Field()
    period = scrapy.Field()
    players_count = scrapy.Field()
    group_url = scrapy.Field()

class PlayerItem(scrapy.Item):
    # define the fields for your item here like:
    ssn = scrapy.Field()
    player_name = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    status = scrapy.Field()
    seminars = scrapy.Field()