from flask import Flask
from flask import render_template
from flask import request

app = Flask("Your Budget Calculator")

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ziel_person = request.form['vorname']
        rueckgabe_string = ziel_person

        return render_template('index.html', name=rueckgabe_string)
    return render_template('index.html')

@app.route('/passt')
def test():
    return "Passt!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
