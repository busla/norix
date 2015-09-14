# NORIX
A spider for <a href="http://www.greidslumidlun.is/">NORI</a>, a centralized club and athlete management system in Iceland. Over 80% of all sports clubs in Iceland use Nori to manage their subscriptions and payment.

The spider is written with <a href="http://scrapy.org/">Scrapy</a> and managed by the ScrapyRT REST api. The spider is launched with ScrapyRT which forwards the payload (club, username, password), logs into Nori and scrapes all data accessible for that user. It then saves the results to MongoDB.

The spider takes the aformentioned parameters and saves the scraped data to db. It therefore doesn´t return any results. To start scraping, you can use the <a href="https://github.com/busla/norix-ui">norix-ui</a> which communicates with <a href="https://github.com/busla/norix-api">norix-api</a> that in turn sends a request to ScrapyRT. Norix-api uses JSON Web Tokens (JWT) to encrypt the password in our DB and sends an authorization token back to the user. You can play with the scraper independantly if you POST the correct payload and then view the results in your Mongo database.


Example:
```
curl 127.0.0.1:9080/crawl.json -d '{"spider_name":"norix", "request": {"url": "http://nameofclub.felog.is/UsersLogin.aspx", "meta": {"user": "yourusername", "password": "yourpassword"}}}'
```

## Install MongoDB
<a href="http://docs.mongodb.org/manual/installation/">Install MongoDB</a>

### OS dependencies
The spider depends on lxml (http://lxml.de/), which in turn depends on the GCC compiler library.

#### OSX
Install XCode.

#### Debian/Ubuntu
This command should do it.
`$ sudo apt-get install python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev`

## Install project.
```
$ git clone https://github.com/busla/norix
$ cd norix/norix
$ which python #slóðin á python 2.7, skrifaðu $python og athugaðu
$ virtualenv -p [slóðin að python] venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ scrapyrt
```

`$ scrapyrt` needs to be launched in the spider project directory (where scrapy.cfg is located).

## Web API
See <a href="https://github.com/busla/norix-api">norix-api</a>

## Web UI
See <a href="https://github.com/busla/norix-ui">norix-ui</a>

