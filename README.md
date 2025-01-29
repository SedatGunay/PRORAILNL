# **Rail NL 🚆**
Deze case behandelt de lijnvoering van intercitytreinen in Nederland. Het doel is om het aantal trajecten binnen een gegeven tijdsframe te maximaliseren. Een **traject** is een route van sporen en stations waarover treinen heen en weer rijden.

## **Case-opdeling**
De case is opgedeeld in twee delen:

### **Deel 1: Noord- en Zuid-Holland**
- Bevat **22 stations** met als doel het creëren van **maximaal zeven trajecten** binnen een tijdsframe van **twee uur**.

### **Deel 2: Nederland**
- Richt zich op de **nationale lijnvoering** met **maximaal 20 trajecten** binnen een tijdsframe van **drie uur**.

## **Kwaliteitsformule**
De kwaliteit van de gegenereerde trajecten wordt beoordeeld aan de hand van de volgende formule:

```
K = p*10000 - (T*100 + Min)
```
Waarbij:
- **K** de totale kwaliteit van de oplossing is.  
- **p** de fractie van bereden verbindingen (waarde tussen 0 en 1).  
- **T** het aantal gebruikte trajecten.  
- **Min** het totale aantal minuten van alle trajecten samen.  

Het doel is om de **hoogst mogelijke K-score** te behalen door optimale trajecten te vinden.

## **📂 Structuur**
De repository is georganiseerd in de volgende mappen:

- **/algorithms**: bevat de geïmplementeerde algoritmen, waaronder:
  - **Greedy Selector**: kiest iteratief de best mogelijke verbinding op basis van een heuristiek.
  - **Hill Climber**: past routes aan en zoekt lokaal naar een betere oplossing.
  - **Randomized Hill Climber**: voegt randomisatie toe om betere oplossingen te verkennen.
  - **Depth First Search**: zoekt diepgaand naar mogelijke trajecten.

- **/classes**: bevat de klassen voor het aanmaken van een treinnetwerk, waaronder:
  - **RailNetwork**: beheert het spoornetwerk en de trajecten.
  - **Station**: representatie van een station.
  - **Connection**: beheert de verbindingen tussen stations.

- **/data**: bevat de *csv*-bestanden van de stations en connecties, georganiseerd per regio:
  - **/data/NL**: gegevens voor het volledige Nederlandse spoornetwerk.
  - **/data/NZ-Holland**: gegevens voor het spoornetwerk van Noord- en Zuid-Holland.

- **/utils**: bevat handige hulpfuncties zoals:
  - **Helper functies** voor dataverwerking.
  - **Scoring functies** om de kwaliteit van trajecten te evalueren.

- **main.py**: het script om het experiment te draaien.

- **visualizer.py**: bevat visualisatiefuncties om de gegenereerde trajecten en netwerken grafisch weer te geven.


## **🛠 Installatie**
Volg deze stappen om het project lokaal te installeren:

1. Clone de repository:
```
git clone https://github.com/SedatGunay/PRORAILNL.git
cd PRORAILNL
```
2. Zorg ervoor dat Python is geïnstalleerd en installeer vervolgens de benodigde pakketten. Er wordt aangeraden om te werken met een virtuele environment 
:
```
pip install -r requirements.txt
```
3. Controleer dat de benodigde *csv*-bestanden aanwezig zijn in de map `data/NL/` en `data/NZ-Holland`.


## **Gebruik**

Om het script uit te voeren, start het hoofdscript `main.py` om het programma te draaien:

```
python main.py
```
Geef vervolgens door middel van het keuzemenu aan welke algoritme er gerunt moet worden.

### **Voorbeeld van een uitvoer**
```
Enter your choice (1/2/3/4/5): 1
The K-score for Greedy optimization is: 6549.0
The optimized trajectories are:
Trajectory 1: Alkmaar -> Castricum -> Zaandam -> Amsterdam Sloterdijk -> Amsterdam Centraal -> Amsterdam Amstel -> Amsterdam Zuid -> Schiphol Airport -> Leiden Centraal -> Den Haag HS -> Delft -> Schiedam Centrum -> Rotterdam Centraal -> Rotterdam Alexander -> Rotterdam Blaak -> Dordrecht -> Breda -> Etten-Leur -> Roosendaal, Duration: 171 minutes
....

Trajectory 18: Amsterdam Amstel -> Utrecht Centraal, Duration: 19 minutes

Trajectory 19: Assen -> Zwolle, Duration: 40 minutes.
```
**LET OP:**  
De experimenten worden gedraaid op het Nationale netwerk, indien er gewerkt wil worden met de NZ-Holland netwerk dient men de 
```
stations_file = 'data/NL/StationsNationaal.csv'
connections_file = 'data/NL/ConnectiesNationaal.csv'
```
aan te passen naar:
```
stations_file = 'data/NZ-Holland/StationsHolland.csv'
connections_file = 'data/NZ-Holland/ConnectiesHolland.csv'
```

Bovendien veranderen de volgende parameters:

- **max_duration**: `180` → `120`
- **Maximale trajecten**: `20` → `7`

Omdat dit onderzoek zich voornamelijk richt op de nationale lijnvoering, zijn de experimenten standaard ingesteld voor het nationale netwerk.
## **Auteurs**
- Fons de Lange
- Dion Koster
- Sedat Günay

