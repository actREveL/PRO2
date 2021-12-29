from flask import Flask
from flask import render_template
from flask import request
import daten
import plotly.express as px
from plotly.offline import plot

app = Flask("Your Budget Calculator")



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return render_template('formular.html')
    return render_template('index.html')

# custom error page
# invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# internal server error url
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

@app.route('/formular', methods=['GET', 'POST'])
def formular():
    if request.method == 'POST':
        name = request.form['name']
        datum = request.form['datum']
        bezeichnung = request.form['bezeichnung']
        kategorie = request.form['kategorie']
        betrag = request.form['betrag']
        notiz = request.form['notiz']

        daten.speichern(name, datum, bezeichnung, kategorie, betrag, notiz)

    return render_template('formular.html')

@app.route('/uebersicht', methods=['GET', 'POST'])
def uebersicht():
    eingabe = daten.eingabe_laden()

    return render_template('uebersicht.html', data=eingabe)

@app.route('/ausgabe')
def ausgabe_monate():
    ausgabe = daten.eingabe_laden()
    monate = {}

    for id, values in ausgabe.items():
        month = values["date"].split(".")[1]
        if not monate.get(month):
            monate[month] = values["sum"]
        else:
            monate[month] = monate[month] + values["sum"]

    x = list(monate.keys())
    y = list(monate.values())

    fig = px.bar(x=x, y=y)
    fig.show()

    return render_template('ausgabe.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
