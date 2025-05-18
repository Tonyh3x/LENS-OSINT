FROM python:3.10-slim

WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Instalacja Python zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie plików aplikacji
COPY . .

# Ustawienie uprawnień
RUN chmod +x entrypoint.sh

# Ustawienie zmiennej środowiskowej
ENV FLASK_APP=app.py

# Uruchomienie aplikacji
ENTRYPOINT ["/app/entrypoint.sh"]
