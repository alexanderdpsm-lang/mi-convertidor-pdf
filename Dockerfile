# Usamos una imagen de Python
FROM python:3.10-slim

# Instalamos LibreOffice (el motor que convierte a PDF)
RUN apt-get update && apt-get install -y libreoffice --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Preparamos la carpeta de trabajo
WORKDIR /app
COPY . /app

# Instalamos las librerías de Python
RUN pip install flask flask-cors

# Iniciamos el servidor
CMD ["python", "app.py"]