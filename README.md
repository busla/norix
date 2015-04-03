# norix
REST vefþjónusta fyrir félagakerfið NORI

NORI er iðkendaskráningakerfi sem haugur af íþróttafélögum á Íslandi er að nota. Norix er REST API sem skilar tilbaka öllum iðkendum sem notandinn hefur aðgang að.

Bakvið Norix er könguló sem loggar sig inn með user og pass frá notandanum, rúllar í gegnum alla hópa og skilar tilbaka öllum iðkendum sem hann hefur aðgang að á JSON sniði.

## Setja upp á localhost (óþarfi nema að þú viljir flippa eitthvað með kóðann)
### Nauðsynlegt
lxml
#### osx
Getur getur verið hausverkur að setja upp, en þú finnur út úr því.

#### Debian/Ubuntu/Mint
`$ sudo apt-get install python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev`

```
git clone https://github.com/busla/norix
cd norix/norix
which python #slóðin á python 2.7, skrifaðu $python og athugaðu
virtualenv -p [slóðin að python] venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

```

## Fá json (til að gera eitthvað gott fönk, vonandi kladda app.)
Í fyrsta skipti sem notandi loggar sig inn ræsir REST-þjónustan spider sem loggar sig inn á Nóra, crawl´ar allt draslið, vistar í DB og skilar tilbaka öllum iðkendum ásamt aukaupplýsingum. Eftir það er alltaf birt iðkendur úr db.

Nota user og pass sem þú fékkst frá félaginu þínu. Ef þú ert t.d. að logga þig inn á https://vikingur.felog.is/ þá notaru bara 'vikingur' sem club parameter.

Demo : http://176.58.105.227:5000/players?club=vikingur&username=randver&password=laukhringur


@Todo
Búa til app til að skrá mætingu.

