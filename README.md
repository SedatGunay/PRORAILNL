# Rail NL 
Deze case behandelt de lijnvoering van intercitytreinen. Het doel is om het aantal trajecten binnen een tijdsframe te maximaliseren. Een traject is een route van sporen en stations waarover treinen heen en weer rijden. 

De case wordt in twee delen gesplits:
* Deel 1: Noord- en Zuid-Holland:

Deze heeft 22 stations met als doel het creëren van maximaal zeven trajecten binnen een tijdsframe van twee uur.

* Deel 2: Nederland
Dit betreft de Nationale lijnuitvoering waarbij er maximaal 20 trajecten zijn binnen een tijdsframe van drie uur

De trajecten worden gescoord op een kwaliteitsformule die als volgt luidt:

```
K = p*10000 - (T*100 + Min)
```
Hierbij is:
* **K** de kwaliteit van de uitvoering 
* **p** de fractie van bereden verbindingen (0-1)
* **T** het aantal trajecten 
* **Min** het aantal minuten van alle trajecten samen

Het doel is dan ook om de trajecten te vinden die de hoogste K- score behalen.


## Structuur

De repository is georganiseerd in de volgende structuur:

- ***/code***: bevat alle code van de case.
    - ***code/algorithms***: bevat de geïmplementeerde algoritmen 
    - ***code/classes***: bevat de classes voor het aanmaken van een treinnetwerk
    - **/code/main.py** : het bestand om het experiment te runnen 
    - **/code/visualizer.py** : het bestand met de visualisatie functies de gebruikt kunnen worden.
- **/data**: bevat de *csv* bestanden van de stations en connecties. 


## Installatie
Volg deze stappen om het project lokaal te installeren:

1. Clone de repository:
```
git clone https://github.com/SedatGunay/PRORAILNL.git 
cd PRORAILNL
```
2. Zorg ervoor dat Python geïnstalleerd is en installeer vervolgens de benodigde pakketten:
```
pip install -r requirements.txt
```
3. Controleer dat de benodigde *csv* bestanden aanwezig zijn in de map data/NL/ en data/NZ-Holland


## Gebruik 

Om het script uit te voeren, start het hoofdscript main.py om het programma te draaien:

```
python main.py
```

Tijdens de uitvoering kunt u kiezen uit de datasets voor Noord- en Zuid-Holland of heel Nederland.

## Experimenten

Het aanpassen van parameters in de code is mogelijk om verschillende distributies van scores te analyseren en zo de beste oplossing te kiezen.

Pas hiervoor de parameters aan in de code van de algoritmen en sla deze resultaten op in CSV-formaat.

Run hierna het visualisatiescript 
```
visualizer.py
``` 
om grafieken te genereren.


## Auteurs 
- Fons de Lange
- Dion Koster
- Sedat Günay
