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
    return render_template('index.html')

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

    return render_template('formular.html')

# Übersichtsseite mit Cards --> holt Infos aus daten.py (Dict) und stellt sie "schön" dar
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
            filter_key = "name"

        elif kategorie != "":
            filter = kategorie
            filter_key = "category"

        elif betrag != "":
            filter = betrag
            filter_key = "sum"

        for key, eintrag in eingabe.items():
            if eintrag[filter_key] == filter:
                filter_liste.append(eintrag)

    return render_template('uebersicht.html', data=eingabe, user=filter_liste)

# Übersichtsseite mit Balkendiagramm
@app.route('/ausgabe')
def statistik():
    ausgabe = daten.eingabe_laden()
    monate = {}

    for id, values in ausgabe.items():
        month = values["Date"].split(".")[1]
        if not monate.get(month):
            monate[month] = float(values["Sum"])
        else:
            monate[month] = monate[month] + float(values["Sum"])

    x = list(monate.keys())
    y = list(monate.values())
    color = ausgabe['name']

    fig = px.bar(x=x, y=y, labels={"x": "Monate",
                                   "y": "Betrag in CHF"},
                 color=color,
                 title="Ausgaben über die Monate hinweg")
    # https://plotly.com/python/figure-labels/ für Benennung der Achsen & Titel,
    # https://careerkarma.com/blog/python-typeerror-unhashable-type-list/ --> für Problembehebung "unhashable list"

    # fig.show() --> erzeugt eigenen Browser, anstelle wurde div (s. Z. 90 verwendet)
    div = plot(fig, output_type="div")

    return render_template('ausgabe.html', viz_div=div)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
