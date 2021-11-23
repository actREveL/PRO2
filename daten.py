import json

def speichern(name, datum, bezeichnung, kategorie, betrag, notiz):
    datei = "uebersicht.json"
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {'name': name,
                        'datum': datum,
                        'bezeichnung': bezeichnung,
                        'kategorie': kategorie,
                        'betrag': betrag,
                        'notiz': notiz}

    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=4)

def eingabe_laden():
    datei_name = "uebersicht.json"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt
