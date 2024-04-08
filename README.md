# Antamina-Challenge-Backend
## Comando para crear la imagen
docker build -t flask-app-antamina .
## Comando para instanciar el contenedor
docker run -d -p 5000:5000 -e DB_USER=root -e DB_PASSWORD=password -e DB_HOST=127.0.0.1 -e DB_NAME=sensors_db -e TRACK_MODIFICATIONS=False flask-app-antamina