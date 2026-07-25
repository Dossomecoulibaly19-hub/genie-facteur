from flask import Flask, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
USERS_ONLINE = {}

@app.route('/')
def home():
    return "✅ SERVEUR GENIECHAT ACTIF"

@socketio.on('join')
def handle_join(data):
    code = data['code']
    USERS_ONLINE[code] = request.sid

@socketio.on('send_message')
def handle_message(data):
    to_code = data['to']
    if to_code in USERS_ONLINE:
        emit('receive_message', data, room=USERS_ONLINE[to_code])

@socketio.on('disconnect')
def handle_disconnect():
    for code, sid in list(USERS_ONLINE.items()):
        if sid == request.sid: del USERS_ONLINE[code]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port)
