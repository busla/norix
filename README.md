# norix
REST vefþjónusta fyrir félagakerfið NORI

NORI er iðkendaskráningakerfi sem haugur af íþróttafélögum á Íslandi er að nota. Norix er REST API sem skilar tilbaka öllum iðkendum sem notandinn hefur aðgang að. Norix geymir ekki neinar notendaupplýsingar heldur sendir user og pass sem parameter til Nora sem sér um allt validation og skilar tilbaka iðkendum eða tómum lista.

Bakvið Norix er könguló sem loggar sig inn með user og pass frá notandanum, rúllar í gegnum alla hópa og skilar tilbaka öllum iðkendum sem hann hefur aðgang að á JSON sniði.

## Setja upp á localhost
Líklega óþarfi nema að þú viljir flippa eitthvað með kóðann sem keyrir bakendann.

### Nauðsynlegt
lxml (http://lxml.de/)

Ef þú ert á osx þá þarftu að setja upp Xcode.
Ef þú ert á Debian/Ubuntu/Mint, þá ætti þetta að duga.
`$ sudo apt-get install python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev`

#### Uppsetning
```
git clone https://github.com/busla/norix
cd norix/norix
which python #slóðin á python 2.7, skrifaðu $python og athugaðu
virtualenv -p [slóðin að python] venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

```

## Fá json
Ef þú ætlar að fönkast eitthvað með niðurstöðurnar... búa til kladda app :-)
Í fyrsta skipti sem notandi loggar sig inn ræsir REST-þjónustan spider sem loggar sig inn á Nóra, crawl´ar allt draslið, vistar í DB og skilar tilbaka öllum iðkendum ásamt aukaupplýsingum. Eftir það er alltaf birt iðkendur úr db.

Nota user og pass sem þú fékkst frá félaginu þínu. Ef þú ert t.d. að logga þig inn á https://breidablik.felog.is/ þá notaru bara 'breidablik' sem club parameter.

Urlið myndi þá líta einhvern veginn svona út:

http://176.58.105.227:5000/players?club=breidablik&username=randver&password=laukhringur

Þetta url virkar auðvitað ekki því ég heiti ekki randver og þjálfa ekki hjá Breiðablik :-P

@Todo
Búa til app til að skrá mætingu.

