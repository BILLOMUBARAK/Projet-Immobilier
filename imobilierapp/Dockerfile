# Dockerfile for Flask application

# Utiliser l'image de base Python 3.9 slim
FROM python:3.9-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires (par exemple, app.py, requirements.txt)
COPY app.py .
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Copier les fichiers HTML et CSS
COPY templates/*.html ./templates/
COPY templates/*.png ./templates/

# Commande par défaut pour exécuter l'application
CMD ["python", "app.py"]
