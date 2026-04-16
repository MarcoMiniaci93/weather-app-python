# weather-app-python
# App Meteo Python - Open-Meteo

## Descrizione

Questa applicazione Python permette di cercare una città e visualizzare:
- il meteo attuale
- la temperatura corrente
- la previsione meteo per i giorni successivi

Il progetto utilizza le API di Open-Meteo per ottenere:
- le coordinate geografiche della città inserita
- i dati meteorologici aggiornati

L'obiettivo del progetto è mettere in pratica:
- l'uso delle API
- la gestione delle richieste HTTP
- l'organizzazione del codice in funzioni
- la formattazione dell'output in modo chiaro e leggibile

## Funzionalità

- Inserimento del nome di una città
- Ricerca automatica della località tramite geocoding
- Visualizzazione del meteo attuale
- Visualizzazione delle previsioni da 3 a 5 giorni
- Traduzione dei codici meteo in descrizioni comprensibili
- Output testuale semplice e ordinato

## Tecnologie utilizzate

- Python
- requests
- pandas
- API Open-Meteo

## Struttura del progetto

- `meteo.py` → file principale dell'app
- `test_meteo.py` → file per i test
- eventuali funzioni di supporto per:
  - descrizione del meteo
  - simboli ASCII
  - formattazione della data in italiano

## Requisiti

Installare le librerie necessarie con:

```bash
pip install requests pandas
```

## Come eseguire il progetto

Avviare il programma con:

```bash
python meteo.py
```

Oppure, se il file principale ha un altro nome:

```bash
python nome_file.py
```

## Come funziona

1. L'utente inserisce il nome della città.
2. Il programma cerca la città tramite API geocoding.
3. Ottiene latitudine e longitudine.
4. Interroga l'API meteo.
5. Mostra il meteo attuale.
6. Mostra la previsione per i giorni scelti.

## Esempio di utilizzo

```text
APP METEO - Open-Meteo
Inserisci il nome della città: Torino
Quanti giorni di previsione? (3-5, invio = 5): 4

TORINO - Meteo attuale
[SOLE] Prevalentemente sereno
Temperatura: 22.0 C

PREVISIONI 4 GIORNI
Gio 16 Apr  MAX 24.2C  MIN 11.4C  [NEBBIA]
Ven 17 Apr  MAX 23.4C  MIN 14.2C  [COPERTO]
Sab 18 Apr  MAX 24.3C  MIN 14.3C  [COPERTO]
Dom 19 Apr  MAX 21.4C  MIN 14.9C  [ROVESCI]
```

## API utilizzate

### Geocoding API
Usata per convertire il nome della città nelle coordinate geografiche.

### Forecast API
Usata per ottenere:
- meteo attuale
- temperatura corrente
- temperature minime e massime giornaliere
- codici meteo e descrizioni

## Punti di forza del progetto

- Codice modulare e leggibile
- Utilizzo di API reali
- Buona separazione tra logica, formattazione e output
- Possibilità di espandere facilmente il progetto

## Possibili miglioramenti

- Interfaccia grafica HTML o Tkinter
- Più dettagli meteo (vento, pioggia, umidità)
- Supporto per più lingue
- Salvataggio delle città preferite
- Icone meteo più avanzate

## Finalità didattica

Questo progetto è stato realizzato per esercitarsi con Python e con l'integrazione di servizi esterni tramite API, migliorando anche la capacità di organizzare il codice e presentare i risultati in modo chiaro.

## Marco Miniaci
Progetto realizzato da [TUO NOME]
