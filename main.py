from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

key = "key12345"

@app.route('/')
def index():
    with open("stazione.txt", "r") as stazionefile:
        temperatura = stazionefile.readlines(1)[0]
        pioggia = stazionefile.readlines(2)[0]
    return render_template("index.html", temperatura=temperatura, pioggia=str(float(pioggia)))

@app.route('/api/stazione', methods=['POST'])
def stazione():
    if request.method == "POST":
        if request.headers['key'] == key:
            temperatura = request.headers['temperatura']
            pioggia = request.headers['pioggia']
            record = pioggia + "\n" + temperatura
            with open("stazione.txt", "w") as stazionefile:
                stazionefile.write(str(record))
            return "200"
        else:
            return "401"
    return "200"

@app.route('/api/temperatura', methods=['GET'])
def temperatura():
    if request.method == "GET":
        with open("stazione.txt", "r") as stazionefile:
            temperatura = stazionefile.readlines(1)[0]
            pioggia = stazionefile.readlines(2)[0]
    return jsonify(pioggia)

@app.route('/admin')
def admin():
    with open("admin.txt", "r") as stazionefile:
        record = stazionefile.readlines()
        temperatura = record[0]
        uptime = record[1]
    return render_template("admin.html", temperatura=temperatura, uptime=uptime)

@app.route('/api/admin', methods=['POST'])
def admin_api():
    if request.method == "POST":
        if request.headers['key'] == key:
            with open("admin.txt", "w") as stazionefile:
                temperatura = request.headers['temperatura']
                temperatura = temperatura.replace(r"\n", "")
                temperatura = temperatura.replace("b'", "")
                temperatura = temperatura.replace("'", "")
                uptime = request.headers['uptime']
                uptime = uptime.replace(r"\n", "")
                uptime = uptime.replace("b'up", "")
                uptime = uptime.replace("'", "")
                record = temperatura + "\n" + uptime
                stazionefile.write(record)
            return "200"
        else:
            return "401"
    return "200"
