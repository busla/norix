# -*- coding: utf-8 -*-

# Scrapy settings for norix project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html

BOT_NAME = 'norix'

SPIDER_MODULES = ['norix.spiders']
NEWSPIDER_MODULE = 'norix.spiders'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'norix (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'norix.pipelines.PlayersPipeline': 100,
    'norix.pipelines.SeminarPipeline': 1000,
    }

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "norix"
MONGODB_COLLECTION = "data"