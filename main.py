from flask import Flask
from flask import render_template
from flask import request
import daten
import plotly.express as px
from plotly.offline import plot

app = Flask("Your Budget Calculator")

"""
Diese Webapplikation wurde selbst gechrieben. Nichts wurde "kopiert". 
Hilfsmittel dabei waren Informationen aus den Vorlesungen von Prog1 & Prog2, vereinzelte Youtube-Tutorials,
Seiten wie bspw. W3Schools oder die Jinga Dokumentation usw., die Boostrap Dokumentation und zu einem grossen Teil die 
jeweiligen Tutoring-Sessions mit F. Odoni und M. Schmid.
"""


# Home / Startseite
@app.route('/', methods=['GET', 'POST'])
def home():
    # wird der Button "Senden" gedrückt, erscheint die Formularseite, sonst normal die Startseite
    if request.method == 'POST':
        return render_template('formular.html')
    return render_template('index.html', user="Samira")  # hier wird der Begrüssungsname mitgegeben (Samira)


# Benutzerdefinierte Fehlerseiten
# Ungültige URL (Seite nicht gefunden)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Interner Serverfehler URL
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Formularseite --> hier können neue Ausgaben erfasst werden
@app.route('/formular', methods=['GET', 'POST'])
def formular():
    if request.method == 'POST':  # nur wenn der Button "Senden" gedrückt wird
        datum = request.form['datum']  # Was im Feld "Datum" eingegeben wurde, wird hiermit aufgerufen usw.
        bezeichnung = request.form['bezeichnung']
        kategorie = request.form['kategorie']
        betrag = request.form['betrag']
        notiz = request.form['notiz']
        # damit werden die eingegebenen Daten gespeichert
        daten.speichern(datum, bezeichnung, kategorie, betrag, notiz)

        eintrag_gespeichert = "Dein Eintrag wurde erfasst. Bei Bedarf kann nun ein weiterer Eintrag erfolgen."

        return render_template('formular.html', eintrag=eintrag_gespeichert)

    # formular.html wird gerendert und zeigt leere Zeilen an, wenn nicht eingegeben.
    # Wird dann jedoch etwas eingegeben und gesendet, werden diese Daten mit daten.speichern (Funktion in daten.py)
    # im Json-file abgespeichert.
    return render_template('formular.html')


# Übersichtsseite mit Cards --> holt Infos aus daten.py (dem Dictionary) und stellt sie "schön" dar
@app.route('/uebersicht', methods=['GET', 'POST'])
def uebersicht():
    eingabe = daten.eingabe_laden()  # holt Daten aus daten.py
    filter_liste = []
    filter_value = ""
    filter_key = ""
    gefiltert = False

    # if-Bedingung, falls gefiltert werden möchte
    if request.method == 'POST':
        gefiltert = True
        kategorie = request.form['kategorie']

        if kategorie != "":
            filter_value = kategorie
            filter_key = "Kategorie"

        for key, eintrag in eingabe.items():  # in dieser for-Schleife wird gefiltert und die leere Liste gefüllt
            if eintrag[filter_key] == filter_value:
                filter_liste.append(eintrag)

    # hier werden die Informationen mitgegeben, die im template "uebersicht" aufgerufen werden können
    return render_template('uebersicht.html', data=eingabe, user=filter_liste, Kat=gefiltert)


# Übersichtsseite mit Balkendiagramm
@app.route('/ausgabe', methods=['GET', 'POST'])
def statistik():
    ausgabe = daten.eingabe_laden()  # Dictionary (alle Daten) von daten.py wird geladen
    monate = {}  # leeres dict für Monate 01-12 (Jan-Dez) definiert, welches mit der unteren for-Schleife gefüllt wird

    for key, values in ausgabe.items():
        month = values["Datum"].split(".")[1]  # Datum splitten, sodass nur Monat (01 = Jan etc.) übrigbleibt

        if not monate.get(month):
            monate[month] = float(values["Betrag"])  # Betrag hinzufügen
        else:
            monate[month] = monate[month] + float(values["Betrag"])  # Betrag hinzufügen und zu Monat addieren

    x = list(monate.keys())  # Liste für Monate --> kann so in Barchart eingelesen werden
    y = list(monate.values())  # Liste für Beträge/Monat --> kann so in Barchart eingelesen werden

    # hier wird der Barchart erstellt bzw. werden die Daten mitgegeben, welche für den Barchart erforderlich sind
    fig = px.bar(x=x, y=y, labels={"x": "Monate",
                                   "y": "Betrag in CHF"},
                 title="Ausgaben über die Monate hinweg")
    # https://plotly.com/python/figure-labels/ für Benennung der Achsen & Titel mittels labels
    # https://careerkarma.com/blog/python-typeerror-unhashable-type-list/ --> für Problembehebung "unhashable list"

    # fig.show() --> erzeugt eigenen Browser, anstelle wurde div (s. Z. 90 verwendet)
    div = plot(fig, output_type="div")

    # Summe berechnen für Total (über alle Monate hinweg)
    sum_liste = list(monate.values())
    summe = 0
    for element in sum_liste:
        summe += float(element)

    # Summe Monat und Budget berechnen
    verfuegbar = 0
    if request.method == 'POST':
        month = request.form['monat']
        sum_monat = monate[month]
        budget_eingabe = float(request.form['budget'])
        budget = budget_eingabe - float(sum_monat)
        verfuegbar = round(verfuegbar + budget, 2)
        # für Funktion "round" --> https://www.delftstack.com/de/howto/python/python-truncate-float-python/

    # rendern des Templates "ausgabe.html" zeigt dann den Barchart an und nimmt Monate und Total mit für die Liste
    # mit den Beiträgen/Monat und die Gesamtausgaben über alle Einträge hinweg
    return render_template('ausgabe.html', viz_div=div, monate=monate, total=summe, ergebnis=verfuegbar)


if __name__ == "__main__":  # Im Browser kann http://127.0.0.1:5000/ aufgerufen werden und die Startseite erscheint.
    app.run(debug=True, port=5000)
