import json
from datetime import datetime

# Funktion, um eingegebene Daten speichern zu können und in einem File abzuspeichern
def speichern(name, datum, bezeichnung, kategorie, betrag, notiz):
    datei = "uebersicht3.json"
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    datei_inhalt[str(datetime.now())] = {'name': name,
                'date': datum,
                'description': bezeichnung,
                'category': kategorie,
                'sum': betrag,
                'notice': notiz}

    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=4)

# Funktion, um gespeicherte Daten laden zu können
def eingabe_laden():
    datei_name = "uebersicht3.json"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt

