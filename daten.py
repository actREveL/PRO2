import json
from datetime import datetime


# Funktion, um eingegebene Daten speichern zu können und in einem File abzuspeichern (Json-File wird geschrieben "w")
def speichern(datum, bezeichnung, kategorie, betrag, notiz):
    datei = "ausgabe_dict.json"
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    datei_inhalt[str(datetime.now())] = {'Datum': datum,
                                         'Bezeichnung': bezeichnung,
                                         'Kategorie': kategorie,
                                         'Betrag': betrag,
                                         'Notiz': notiz}

    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=4)


# Funktion, um gespeicherte Daten (vom Json-File) laden zu können
def eingabe_laden():
    datei_name = "ausgabe_dict.json"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt
