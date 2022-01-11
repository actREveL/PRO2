from flask import Flask
from flask import render_template
from flask import request
import daten
import plotly.express as px
from plotly.offline import plot

app = Flask("Your Budget Calculator")

# Home / Startseite
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return render_template('formular.html')
    return render_template('index.html', user="Samira")

# Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error URL
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Formularseite --> hier können neue Ausgaben angegeben werden
@app.route('/formular', methods=['GET', 'POST'])
def formular():
    if request.method == 'POST':
        name = request.form['name']
        datum = request.form['datum']
        bezeichnung = request.form['bezeichnung']
        kategorie = request.form['kategorie']
        betrag = request.form['betrag']
        notiz = request.form['notiz']
        # eigegebene Daten werden gespeichert
        daten.speichern(name, datum, bezeichnung, kategorie, betrag, notiz)

    # formular.html wird gerendert und zeigt leere Zeilen an, wenn nicht eingegeben. Wird dann jedoch etwas eingegeben und gesendet, werden diese Daten mit daten.speichern (Funktion in daten.py) im json-file abgespeichert.
    return render_template('formular.html')

# Übersichtsseite mit Cards --> holt Infos aus daten.py (dem Dictionary) und stellt sie "schön" dar
@app.route('/uebersicht', methods=['GET', 'POST'])
def uebersicht():
    eingabe = daten.eingabe_laden()
    filter_liste = []

    if request.method == 'POST':
        name = request.form['name']
        kategorie = request.form['kategorie']
        betrag = request.form['betrag']

        if name != "":
            filter = name
            filter_key = "Name"

        elif kategorie != "":
            filter = kategorie
            filter_key = "Kategorie"

        elif betrag != "":
            filter = betrag
            filter_key = "Betrag"

        for key, eintrag in eingabe.items():
            if eintrag[filter_key] == filter:
                filter_liste.append(eintrag)




    return render_template('uebersicht.html', data=eingabe, user=filter_liste)

# Übersichtsseite mit Balkendiagramm
@app.route('/ausgabe')
def statistik():
    ausgabe = daten.eingabe_laden() # Dictionary (alle Daten) von daten.py wird geladen
    monate = {} # leeres dict für Monate 01-12 (Jan-Dez) definiert, welches mit der unteren for-Schleife gefüllt wird

    for id, values in ausgabe.items():
        month = values["Datum"].split(".")[1] # Datum splitten, sodass nur Monat (01 = Jan etc.) übrigbleibt

        if not monate.get(month):
            monate[month] = float(values["Betrag"]) # Betrag hinzufügen
        else:
            monate[month] = monate[month] + float(values["Betrag"]) # Betrag hinzufügen und zu Monat addieren

    x = list(monate.keys()) # Liste für Monate --> kann so in Barchart eingelesen werden
    y = list(monate.values()) # Liste für Beträge/Monat --> kann so in Barchart eingelesen werden
    # nutzer = ausgabe["Name"] --> wieso funktioniert das nicht?!

    # hier wird der Barchart erstellt bzw. werden die Daten mitgegeben, welche für den Barchart erforderlich sind
    fig = px.bar(x=x, y=y, labels={"x": "Monate",
                                   "y": "Betrag in CHF"},
                 # color=nutzer,
                 title="Ausgaben über die Monate hinweg")
    # https://plotly.com/python/figure-labels/ für Benennung der Achsen & Titel mittels labels
    # https://careerkarma.com/blog/python-typeerror-unhashable-type-list/ --> für Problembehebung "unhashable list"

    # fig.show() --> erzeugt eigenen Browser, anstelle wurde div (s. Z. 90 verwendet)
    div = plot(fig, output_type="div")

    # Summe berechnen für Total (über alle Monate hinweg)
    sum_liste = list(monate.values())
    sum = 0
    for element in sum_liste:
        sum+=float(element)

    # rendern des Templates "ausgabe.html" zeigt dann den Barchart an und nimmt monate und total mit für die Liste mit den Beiträgen/Monat und die Gesamtausgaben über alle Einträge hinweg
    return render_template('ausgabe.html', viz_div=div, monate=monate, total=sum)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
