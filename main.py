from flask import Flask
from flask import render_template
from flask import request

app = Flask("Your Budget Calculator")


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name_person = request.form['name']
        rueckgabe_string_name = name_person
        name_datum = request.form['datum']
        rueckgabe_string_datum = name_datum
        name_bezeichnung = request.form['bezeichnung']
        rueckgabe_string_bezeichnung = name_bezeichnung
        name_kategorie = request.form['kategorie']
        rueckgabe_string_kategorie = name_kategorie
        name_betrag = request.form['betrag']
        rueckgabe_string_betrag = name_betrag
        name_betrag2 = request.form['betrag2']
        rueckgabe_string_betrag2 = name_betrag2
        name_betrag3 = request.form['betrag3']
        rueckgabe_string_betrag3 = name_betrag3
        name_notiz = request.form['notiz']
        rueckgabe_string_notiz = name_notiz


        # Variablen, Funktionen etc. oder auch abspeichern

        return render_template('ausgaben.html',
                               name=rueckgabe_string_name,
                               datum=rueckgabe_string_datum,
                               bezeichnung=rueckgabe_string_bezeichnung,
                               kategorie=rueckgabe_string_kategorie,
                               betrag=rueckgabe_string_betrag,
                               betrag2=rueckgabe_string_betrag2,
                               betrag3=rueckgabe_string_betrag3,
                               notiz=rueckgabe_string_notiz)

    return render_template("index.html")


@app.route('/passt')
def test():
    return "Passt!"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
