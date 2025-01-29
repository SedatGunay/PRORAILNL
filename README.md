# Rail NL
Deze case behandelt de lijnvoering van intercitytreinen. Het doel is om het aantal trajecten binnen een tijdsframe te maximaliseren. Een traject is een route van sporen en stations waarover treinen heen en weer rijden.

De case wordt in twee delen gesplitst:
* **Deel 1: Noord- en Zuid-Holland**
  - 22 stations met als doel het creëren van maximaal zeven trajecten binnen een tijdsframe van twee uur.
* **Deel 2: Nederland**
  - De nationale lijnuitvoering met maximaal 20 trajecten binnen een tijdsframe van drie uur.

De trajecten worden gescoord op een kwaliteitsformule:

```
K = p*10000 - (T*100 + Min)
```
Hierbij is:
* **K** de kwaliteit van de uitvoering
* **p** de fractie van bereden verbindingen (0-1)
* **T** het aantal trajecten
* **Min** het aantal minuten van alle trajecten samen

Het doel is om de trajecten te vinden die de hoogste K-score behalen.

---
## **Structuur**

De repository is georganiseerd in de volgende structuur:

- **/code**: bevat alle code van de case.
  - **/code/algorithms**: bevat de geïmplementeerde algoritmen, waaronder:
    - **Greedy Selector**: kiest iteratief de best mogelijke verbinding op basis van een heuristiek.
    - **Hill Climber**: past routes aan en zoekt lokaal naar een betere oplossing.
    - **Randomized Hill Climber**: voegt randomisatie toe om betere oplossingen te verkennen.
    - **Depth First Search**: zoekt diepgaand naar mogelijke trajecten.
  - **/code/classes**: bevat de klassen voor het aanmaken van een treinnetwerk, zoals `RailNetwork`, `Station`, en `Connection`.
  - **/code/main.py**: het script om het experiment te draaien.
  - **/code/visualizer.py**: visualisatiefuncties om de gegenereerde trajecten weer te geven.
- **/data**: bevat de *csv*-bestanden van de stations en connecties.

---
## **Installatie**
Volg deze stappen om het project lokaal te installeren:

1. Clone de repository:
```
git clone https://github.com/SedatGunay/PRORAILNL.git
cd PRORAILNL
```
2. Zorg ervoor dat Python is geïnstalleerd en installeer vervolgens de benodigde pakketten:
```
pip install -r requirements.txt
```
3. Controleer dat de benodigde *csv*-bestanden aanwezig zijn in de map `data/NL/` en `data/NZ-Holland`.

---
## **Gebruik**

Om het script uit te voeren, start het hoofdscript `main.py` om het programma te draaien:

```
python main.py
```
Tijdens de uitvoering kunt u kiezen uit de datasets voor Noord- en Zuid-Holland of heel Nederland.


### **Voorbeeld van een uitvoer**
```
Traject 1: Station A -> Station B -> Station C (45 min)
Traject 2: Station D -> Station E -> Station F (37 min)
...
Kwaliteitsscore: 12.540
```

---
## **Experimenten**
Het aanpassen van parameters in de code is mogelijk om verschillende distributies van scores te analyseren en zo de beste oplossing te kiezen.

LET OP de parameters voor max-limit (tijdsduur) verschilt voor Nederland en Noord- en Zuid-Holland, dit zal handmatig aangepast moeten worden om de algoritmen op de juiste manier te kunnen runnen.

1. Pas de parameters aan in de code van de algoritmen.
2. Sla de resultaten op in CSV-formaat.

3. Voer het visualisatiescript uit om grafieken te genereren:
```
python visualizer.py
```

---
## **Auteurs**
- Fons de Lange
- Dion Koster
- Sedat Günay

