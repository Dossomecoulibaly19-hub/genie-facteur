from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

app = Flask(__name__)
# FIX 1: On passe en threading. Plus stable sur Render gratuit que eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
USERS_ONLINE = {}

@app.route('/')
def home():
    return "✅ SERVEUR GENIECHAT ACTIF"

@socketio.on('join')
def handle_join(data):
    code = data['code']
    sid = request.sid
    USERS_ONLINE[code] = sid
    join_room(sid) # FIX 2: On met le sid dans une room pour pouvoir lui envoyer
    print(f"[JOIN] {code} -> {sid}")

@socketio.on('send_message')
def handle_message(data):
    to_code = data['to']
    print(f"[SEND] {data['from']} -> {to_code}")

    # On sauvegarde d'abord côté serveur principal
    # Le serveur principal fait déjà ça, donc on relaie juste

    if to_code in USERS_ONLINE:
        target_sid = USERS_ONLINE[to_code]
        # FIX 3: On envoie aux 2 events
        emit('receive_message', data, room=target_sid)
        emit('new_message_alert', {}, room=target_sid) # Pour que l'app reload
    else:
        print(f"[OFFLINE] {to_code} n'est pas connecté")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    for code, s in list(USERS_ONLINE.items()):
        if s == sid:
            del USERS_ONLINE[code]
            leave_room(sid) # FIX 4: On quitte la room
            print(f"[LEAVE] {code}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port)
