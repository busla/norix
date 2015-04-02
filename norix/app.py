#!flask/bin/python
from flask import Flask
from norix.spiders.norix_spider import NorixSpider
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/practitioners', methods=['GET'])
def get_practitioners():
    spider = NorixSpider(url='http://umfg.felog.is', domain='umfg.felog.is')
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run(installSignalHandlers=0) # the script will block here until the spider_closed signal was sent        

    return spider.export

if __name__ == '__main__':
    app.run(debug=True)
