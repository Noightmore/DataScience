# Informace k projektu

## Instalace a spousteni

Je silne doporuceno pouzit python verzi 3.11.
Postup instalace a spusteni skriptu je popsan pro bash shell, pokud neni pouzit WSL (windows subsystem for linux) 
je nutne pouzit jiný z mnoha windows postupů: https://virtualenv.pypa.io/en/latest/installation.html

Zprovozneni prostredi a zpusteni skriptu (venv vytvorime ve slozce PZR):

```python -m venv venv```

```source venv/bin/activate```

```pip install -r requirements.txt```

```python ./cv1/time_to_speech.py```


Spusteni jupyter notebooku:

```cd cv1```

```jupyter notebook```

Jupyter notebook je dostupny na adrese: http://localhost:8888/

## Popis projektu

Nahravky byly schválně pořízeny sekvenčně po jedné za sebou pomocí skriptu ```record.sh```. 
Toto není nejoptimálnější způsob pořízení, avšak jsem se nahrávky
pokusil co nejvíce ošetřit softwarově. Oříznutím ticha na konci a na začátku nahrávky, normalizací hlasitostí 
na předem nastavenou úroveň, zvýšením hlasitosti (nahraní bylo velmi tiché) a pokusem o odstranení plosivních zvuků 
(například písmena "t" ve slově "minut")

Nahrávky byly uloženy ve formátu ".opus", jedná se o ztrátovou kompresi audia u právě nahrávek hlasu/hudby.
Komprese je vyšší než u mp3, ale s minimálním rozdílem ve kvalitě. Velikost celé složky s nahrávkami je skoro 150 KiB.
Program umožnuje i stáhnutí datasetu nahrávek z huggingface.


## Popis skriptů

Pokud by z jakéhokoliv důvodu nebylo možné spustit jupyter notebook, lze spustit skript time_to_speech.py,
který obsahuje základní funkcionalitu. Jupyter notebook rozšiřuje obsah o možnost kreslení grafů a obsahuje detailnější
postup vývoje včetné dalších pokusů o implementaci jednotlivých částí programu.