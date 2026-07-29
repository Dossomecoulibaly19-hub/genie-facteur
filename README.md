# genie-facteur
Serveur Central de GenieChat

Serveur WebSocket pour relayer les messages en temps réel entre les utilisateurs de GenieChat.

### Fonctionnement
1. Chaque client se connecte avec son `code` via `socket.emit('join', {code})`
2. Quand un user envoie `socket.emit('send_message', data)` le serveur relaye à l'autre
3. Stockage principal se fait sur le serveur Flask principal `genichat-v2`

### Déploiement Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --worker-class eventlet -w 1 server:app`

### Requirements.txt
