# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from scrapy.item import Field


class ClubItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()

class DepartmentItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()

class SeminarItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    sport_department = scrapy.Field()
    name = scrapy.Field()
    group = scrapy.Field()
    period = scrapy.Field()
    players_count = scrapy.Field()
    group_url = scrapy.Field()

class PlayerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()

