#!/bin/bash

echo "=== Verificando Gunicorn ==="
systemctl is-active --quiet onchainkms && echo "✅ Servicio Gunicorn activo" || echo "❌ Servicio Gunicorn detenido"

echo ""
echo "=== Probando Flask directamente ==="
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/ranking | grep -q 200 && echo "✅ Flask responde OK" || echo "❌ Flask no responde"

echo ""
echo "=== Probando Nginx + proxy API ==="
curl -s -o /dev/null -w "%{http_code}" https://onchainkms.baseminiapps.com/api/ranking | grep -q 200 && echo "✅ Nginx proxy responde OK" || echo "❌ Nginx proxy falla (502/403/etc.)"

echo ""
echo "=== Comprobando logs recientes Gunicorn ==="
journalctl -u onchainkms -n 5 --no-pager
