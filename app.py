from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": "user", "message": message})
    return jsonify(response.json())

@socketio.on('message')
def handle_message(message):
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": "user", "message": message})
    response_data = response.json()
    if response_data:
        emit('bot_response', response_data[0]['text'])

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
