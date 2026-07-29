# genie-facteur
Serveur Central de GenieChat

### Déploiement Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --worker-class eventlet -w 1 server:app`
