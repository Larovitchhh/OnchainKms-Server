#!/bin/bash
# start_backend.sh
# Script para reiniciar el backend de OnChainKms

# 1️⃣ Matar procesos antiguos de gunicorn o app.py
echo "⏹ Deteniendo procesos antiguos..."
pkill -f gunicorn
pkill -f app.py

# 2️⃣ Esperar un par de segundos para liberar el puerto
sleep 2

# 3️⃣ Arrancar el backend con gunicorn
echo "🚀 Iniciando backend con gunicorn..."
cd /root/onchainkms/backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
