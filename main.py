from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open("stazione.txt", "r") as stazionefile:
        temperatura = stazionefile.readlines(1)[0]
        pioggia = stazionefile.readlines(2)[0]
    return render_template("index.html", temperatura=temperatura, pioggia=pioggia)

@app.route('/api/stazione', methods=['POST'])
def stazione():
    if request.method == "POST":
        temperatura = request.headers['temperatura']
        pioggia = request.headers['pioggia']
        record = pioggia + "\n" + temperatura
        with open("stazione.txt", "w") as stazionefile:
            stazionefile.write(str(record))
        return "ok"

app.run(host="localhost")
