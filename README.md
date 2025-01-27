# Rail NL 
Deze case behandelt de lijnvoering van intercitytreinen. Het doel is om het aantall trajecten binnen een tijdsframe te maximaliseren. Er zijn twee versies van het probleem:
de eerste gaat over de provinces Noord- en Zuid- Holland en de tweede over heel Nederland. 

## Vereisten

Deze codebase is volledig geschreven in Python 3.7. In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

Of via conda:

```
conda install --file requirements.txt
```

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
