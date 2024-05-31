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
    rasa_response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": message})
    return jsonify(rasa_response.json())

@socketio.on('message')
def handle_message(message):
    emit('message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
