#!/bin/sh

# Sprawdzenie czy wszystkie pliki istnieją
if [ ! -d "uploads" ]; then
    mkdir -p uploads
fi

if [ ! -d "reports" ]; then
    mkdir -p reports
fi

if [ ! -d "logs" ]; then
    mkdir -p logs
fi

# Ustawienie uprawnień
chown -R www-data:www-data uploads reports logs

# Uruchomienie aplikacji
exec gunicorn -w 4 -b 0.0.0.0:5000 app:app
