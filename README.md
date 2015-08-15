# norix
REST vefþjónusta fyrir félagakerfið NORI

NORI er iðkendaskráningakerfi sem haugur af íþróttafélögum á Íslandi er að nota. Norix er REST API sem skilar tilbaka öllum iðkendum sem notandinn hefur aðgang að. Norix geymir ekki neinar notendaupplýsingar heldur sendir user og pass sem parameter til Nora sem sér um allt validation og skilar tilbaka iðkendum eða tómum lista.

Bakvið Norix er könguló sem loggar sig inn með user og pass frá notandanum, rúllar í gegnum alla hópa og skilar tilbaka öllum iðkendum sem hann hefur aðgang að á JSON sniði.

## Setja upp MongoDB
<a href="http://docs.mongodb.org/manual/installation/">Install MongoDB</a>

### Nauðsynlegt
Köngulóin dependar á lxml (http://lxml.de/)

Ef þú ert á osx þá þarftu að setja upp Xcode til að fá lxml.
Ef þú ert á Debian/Ubuntu/Mint, þá ætti þessi skipun að duga.
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

## REST þjónustan
Í fyrsta skipti sem notandi loggar sig inn ræsir REST-þjónustan könguló sem loggar sig inn á Nóra, crawl´ar allt draslið, vistar í DB og skilar tilbaka öllum iðkendum ásamt aukaupplýsingum. Eftir það eru iðkendur alltaf birtir úr db og köngulóin fær að hvíla sig.

Til að Norix geti skilað þér einhverju þarftu að nota notandanafnið og lykilorðið sem þú fékkst úthlutað frá félaginu þínu. Ef þú ert þjálfari sem loggar sig inn á https://breidablik.felog.is/starfsmenn þá notaru 'breidablik' sem club parameter og svo notandanafnið þitt og lykilorðið.

Sem dæm, þá myndi urlið líta einhvern veginn svona út:

http://176.58.105.227:5000/players?club=breidablik&username=randver&password=laukhringur

Þetta url virkar auðvitað ekki því ég heiti ekki randver og þjálfa ekki hjá Breiðablik :-P

## Vefviðmót
Ef þú vilt fá meira fönk en bara json, þá geturu ræst einfalt vefviðmót með eftirfarandi skipun:
`$ cd ui && grunt server`

Athugaðu að þú þarft að vera með <a href="https://nodejs.org/">Node</a> uppsett.


@Todo
Búa til app til að skrá mætingu.

