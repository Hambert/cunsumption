from flask import Flask, request, render_template, redirect, url_for, abort
import redis
import json
from datetime import datetime
import os



app = Flask(__name__)
#db = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

env_DB_URL = os.environ.get('DB_URL', None)
env_DB_PW = os.environ.get('DB_PW', None)

if env_DB_PW and env_DB_URL is not None:
    db = redis.Redis(
    host=env_DB_URL,
    port=40409,
    password=env_DB_PW,
    decode_responses=True
    )
    envOk = True
else:
    # Check environment Variables
    envOk = False

@app.route('/')
def form():
    if envOk:
        return render_template('form.html')  # Stellen Sie sicher, dass form.html im "templates"-Verzeichnis liegt.
    else:
        return abort(500)

@app.route('/input', methods=['POST'])
def speichern():
    if request.method == 'POST':
        # Daten von Formular empfangen
        datum = request.form['datum']
        menge = request.form['menge']
        kmstand = request.form['kmstand']
        preis = request.form['preis']
        
        # Erstellen eines einzigartigen Schlüssels für diesen Eintrag
        key = f"Eintrag:{datetime.now().timestamp()}"
        
        # Daten als JSON speichern
        data = {'datum': datum, 'menge': menge, 'kmstand': kmstand, 'preis': preis}
        db.set(key, json.dumps(data))

        return redirect(url_for('viewData'))

@app.route('/view')
def viewData():
    # Alle Schlüssel abrufen, die mit "Eintrag:" beginnen
    keys = db.keys('Eintrag:*')

    # Alle Daten abrufen
    eintraege = []
    for key in keys:
        eintrag = json.loads(db.get(key))
        eintraege.append(eintrag)

    # Daten an das 'table.html' Template weitergeben
    return render_template('table.html', eintraege=eintraege)  # Daten in einer Tabellep darstellen.

if __name__ == '__main__':
    app.run(debug=True)