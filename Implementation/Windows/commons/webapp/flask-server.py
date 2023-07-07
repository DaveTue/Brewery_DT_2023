from flask import Flask, request, abort
from kafka import KafkaProducer
from datetime import datetime
import json
import requests

switch = False
producer = KafkaProducer(bootstrap_servers='localhost:9092')
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return ('access successfully.', 200, None)

@app.route('/plaato', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        message = json.dumps(request.json)
        producer.send('plaato2', message.encode())
        return 'success', 200
    else:
        abort(400)

@app.route('/tilt', methods=['POST'])
def tilt():
    if request.method == 'POST':
        print(request.json)
        message = json.dumps(request.json)
        producer.send('tilt2', message.encode())
        return 'success', 200
    else:
        abort(400)

@app.route('/inkbird', methods=['POST'])
def inkbird():
    if request.method == 'POST':
        print(request.json)
        message = json.dumps(request.json)
        producer.send('inkbird2', message.encode())
        return 'success', 200
    else:
        abort(400)

@app.route('/pump', methods=['POST'])
def pump():
    global switch
    if request.method == 'POST':
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(request.json)
        command = bool(int(request.json['command']))
        if command and (command ^ switch):
            switch = True
            rep = requests.post('https://maker.ifttt.com/trigger/switchOn/with/key/dN0ME9Vp141sRSGWXRxKzfm29wQOp_iprJW8AhlG5dK')
            print(dt_string, 'SWITCH ON', rep)
        if not command and (command ^ switch):
            switch = False
            rep = requests.post('https://maker.ifttt.com/trigger/switchOff/with/key/dN0ME9Vp141sRSGWXRxKzfm29wQOp_iprJW8AhlG5dK')
            print(dt_string, 'SWITCH OFF', rep)
        return 'success', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0')