from flask import Flask
from flask import render_template
from flask import request
import daten

app = Flask("Your Budget Calculator")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return render_template('formular.html')
    return render_template('index.html')


@app.route("/liste")
def auflisten():
    eingabe = daten.eingabe_laden()
    eingabe_liste = ""
    for key, value in eingabe.items():
        zeile = str(key) + ": " + value + "<br>"
        eingabe_liste += zeile
    return eingabe_liste

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


# @app.route('/ausgabe')
# def ausgabe():
#     if form.validate_on_submit() == 'POST':
#         if 'yes' in request.form:
#             return render_template('uebersicht.html')
#         elif 'no' in request.form:
#             return render_template('formular.html')
#     return render_template('ausgabe.html')

@app.route('/uebersicht')
def uebersicht():
    daten.eingabe_laden()
    return render_template('uebersicht.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
