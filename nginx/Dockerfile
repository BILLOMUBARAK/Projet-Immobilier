# Utiliser l'image de base NGINX
FROM nginx:latest

# Supprimer le fichier de configuration par défaut de NGINX
RUN rm /etc/nginx/conf.d/default.conf

# Copier votre fichier de configuration personnalisé
COPY nginx.conf /etc/nginx/conf.d/

# Exposer le port 80
EXPOSE 80

# Commande par défaut pour démarrer NGINX
CMD ["nginx", "-g", "daemon off;"]
