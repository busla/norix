# norix
REST vefþjónusta fyrir félagakerfið NORI

<a href="http://www.greidslumidlun.is/">NORI</a> er iðkendaskráningakerfi frá fyrirtækinu Greiðslumiðlun sem haugur af íþróttafélögum á Íslandi er að nota. Norix er REST API sem skilar tilbaka öllum iðkendum sem notandinn hefur aðgang að. Norix geymir nafn, kennitölu og hópinn sem iðkandinn er í. Þetta er gert til að þurfa ekki að kalla í Nora í hvert skipti sem notandinn vill sjá lista yfir iðkendur.

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

http://localhost:5000/players?club=breidablik&username=randver&password=laukhringur

Þetta url virkar auðvitað ekki því ég heiti ekki randver og þjálfa ekki hjá Breiðablik :-P

## Vefviðmót
Setur club, user og pass inn hér:
https://github.com/busla/norix/blob/master/ui/app/scripts/controllers/main.js

Settu upp <a href="https://nodejs.org/">Node</a>.

Ræsir viðmótið með:
`$ cd ui && grunt server`

Þetta gerir ekkert nema birta alla iðkendur sem þú hefur aðgang að. Ég efast um að einhver sé að nota mætingarlistana í NORA og svo næst á dasgskrá er að bæta við kladda-fídus til að skrá mætingu í vefappinu og dúndra því tilbaka með könguló í NORA.

Hvað svo? Mobile-app svo þjálfarar geti tekið mætingu í símanum á æfingu?
