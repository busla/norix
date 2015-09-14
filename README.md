# NORIX
A spider for <a href="http://www.greidslumidlun.is/">NORI</a>, a centralized club and athlete management and payment system in Iceland. Over 80% of all sports clubs in Iceland use Nori to manage their subscriptions and payment.

The spider is written with <a href="http://scrapy.org/">Scrapy</a> and managed by the ScrapyRT REST api. The spider is launched with ScrapyRT which forwards the payload (club, username, password), logs into Nori and scrapes all data accessible for that user. It then saves the results to MongoDB.


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

