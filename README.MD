# The Big O-Block

Čūskas spēle ar Pygame. Rezultāti tiek sūtīti uz paša rakstītu serveri (FastAPI + SQLite), kas rāda līderu tabulu un spēlētāju statistiku mājaslapā.

PB2 prakses uzdevums "Spēle ar savu serveri", grupa P25-2.

## Kā sākt spēlēt

Vajag Python 3.11 vai jaunāku. Visas komandas izpildi projekta mapē.

**1. Uzstādīšana (tikai pirmo reizi)**

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS un Linux: `source .venv/bin/activate`

**2. Palaid serveri** (pirmajā terminālī, atstāj to atvērtu)

```
uvicorn api.main:app --reload
```

**3. Palaid spēli** (otrajā terminālī, ar aktivizētu `.venv`)

```
python -m client.main
```

**4. Spēlē**

Ievadi savu vārdu un nospied Enter. Kad spēle beidzas, rezultāts automātiski aiziet uz serveri. Ja serveris nav ieslēgts, spēle turpina darboties, bet rezultāts netiek saglabāts.

**5. Apskati rezultātus pārlūkā**

Atver http://127.0.0.1:8000 - tur ir TOP tabula. Noklikšķini uz spēlētāja vārda, lai redzētu visas viņa spēles un statistiku.

## Vadība

|        Taustiņš      |     Darbība     |
|----------------------|-----------------|
| W A S D vai bultiņas | Čūskas virziens |
|         Space        | Matrix efekts   |
|           P          | Pauze           |
|           R          | Jauna spēle     |
|           Esc        | Iziet           |

Zelta ābols (5% iespēja) dod 150 punktus parastā ābola 10 vietā. Ik pēc 150 punktiem sākas nākamais līmenis un čūska kļūst ātrāka (6 līmeņi).

## Mājaslapa

|       Adrese      |                   Saturs                      |
|-------------------|-----------------------------------------------|
| `/`               | Līderu tabula (labākie 5 rezultāti)           |
| `/players/{name}` | Spēlētāja profils: visas spēles un statistika |
| `/rules`          | Spēles noteikumi                              |

## REST API

Dokumentācija un testēšana: http://127.0.0.1:8000/docs

| Metode |          Adrese          |                               Ko dara                          | Veiksmīga atbilde |
|--------|--------------------------|----------------------------------------------------------------|-------------------|
|  POST  | `/scores`                | Saglabā rezultātu, piemēram `{"player": "Anna", "score": 120}` |        201        |
|   GET  | `/scores/top`            | Atdod 5 labākos rezultātus                                     |        200        |
|   GET  | `/players/{name}/stats`  | Spēlētāja statistika (spēles, labākais rezultāts)              |      200 / 404    |

Vārds ir no 1 līdz 20 simboliem, punkti nav negatīvi. Nederīgi dati netiek ierakstīti datubāzē, serveris atbild ar 422. Datubāzes fails `game.db` izveidojas pats.

