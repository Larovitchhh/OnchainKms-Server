from flask import Flask, jsonify, send_from_directory
from strava_service import get_monthly_ranking
import os

# Carpeta donde está tu frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '../frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR)

# --- Rutas ---
@app.route('/')
def home():
    # Sirve index.html del frontend
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/ranking')
def ranking():
    """Endpoint que obtiene el ranking mensual desde Strava"""
    try:
        data = get_monthly_ranking()
        if not data or "ranking" not in data:
            return jsonify({"error": "No se pudo obtener el ranking"}), 500
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Ejecutar la app ---
if __name__ == '__main__':
    # Flask escuchará en todas las interfaces
    app.run(host='0.0.0.0', port=5000)
