from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
# threading = plus stable en local, eventlet = obligatoire sur Render
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', logger=True, engineio_logger=True)
USERS_ONLINE = {}

@app.route('/')
def home():
    return "✅ SERVEUR GENIECHAT ACTIF"

@socketio.on('join')
def handle_join(data):
    code = data['code'].upper()
    sid = request.sid
    USERS_ONLINE[code] = sid
    join_room(sid) # CRITIQUE: pour pouvoir envoyer au sid
    print(f"[JOIN] {code} connecté avec SID {sid}")

@socketio.on('send_message')
def handle_message(data):
    to_code = data['to'].upper()
    print(f"[SEND] {data['from']} -> {to_code}")

    if to_code in USERS_ONLINE:
        target_sid = USERS_ONLINE[to_code]
        emit('receive_message', data, room=target_sid)
        emit('new_message_alert', {}, room=target_sid) # pour reload l'app
    else:
        print(f"[OFFLINE] {to_code} n'est pas connecté")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    for code, s in list(USERS_ONLINE.items()):
        if s == sid:
            del USERS_ONLINE[code]
            leave_room(sid)
            print(f"[LEAVE] {code} déconnecté")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port)
