import os
import json
import requests
from datetime import datetime, timedelta, timezone

# --- CONFIGURACIÓN ---
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN", "eb6d80e6f9ee74ea61618bc69f1984cfc00fe0d8")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN", "7b425c2090e2bb60e2af064873f7b2539b7ea51d")
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID", "182742")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET", "c8625a40a4186c1030872d5585bd6ab16c765954")
CLUB_ID = os.getenv("STRAVA_CLUB_ID", "1814151")  # tu club real

STRAVA_API_URL = "https://www.strava.com/api/v3"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data", "ranking.json")


# --- FUNCIONES ---
def refresh_access_token():
    """Renueva el token de acceso de Strava si ha expirado"""
    global ACCESS_TOKEN, REFRESH_TOKEN
    url = f"{STRAVA_API_URL}/oauth/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    r = requests.post(url, data=data)
    print("======== refresh_access_token ========")
    print("POST data:", {**data, "client_secret": "***", "refresh_token": "***"})
    print("Status:", r.status_code)
    if r.status_code == 200:
        tokens = r.json()
        print("🔥 Token refresh OK")
        ACCESS_TOKEN = tokens["access_token"]
        REFRESH_TOKEN = tokens["refresh_token"]
        return ACCESS_TOKEN
    else:
        print("⚠️ Error renovando el token:", r.text)
        return ACCESS_TOKEN


def get_club_activities():
    """Obtiene las actividades del club"""
    global ACCESS_TOKEN
    print("\n======== get_club_activities ========")
    print(f"Usando ACCESS_TOKEN: {ACCESS_TOKEN[:10]}...")

    url = f"{STRAVA_API_URL}/clubs/{CLUB_ID}/activities"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"per_page": 50}
    r = requests.get(url, headers=headers, params=params)
    print("→ GET", r.url)
    print("←", r.status_code, r.reason)

    if r.status_code == 401:
        print("401: token inválido, intentar refresh\n")
        ACCESS_TOKEN = refresh_access_token()
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        r = requests.get(url, headers=headers, params=params)

    if r.status_code != 200:
        print("❌ Error accediendo al club:", r.text)
        return []

    activities = r.json()
    print("Total actividades obtenidas:", len(activities))
    return activities


def get_monthly_ranking():
    """Genera el ranking de los últimos 30 días"""
    print("\n🏁 Generando ranking mensual desde Strava...\n")

    activities = get_club_activities()
    if not activities:
        data = {"last_update": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), "ranking": []}
        save_ranking(data)
        return data

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
    ranking = {}

    for a in activities:
        athlete = a.get("athlete", {}).get("firstname", "Desconocido")
        distance_km = a.get("distance", 0) / 1000
        sport = a.get("sport_type", "")
        created_at = a.get("created_at") or a.get("start_date")

        # intentar usar created_at si no hay start_date
        try:
            date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except Exception:
            date = cutoff_date  # fallback

        if date < cutoff_date:
            continue
        if distance_km <= 0:
            continue
        if sport not in ["Ride", "Run", "Hike", "MountainBikeRide", "GravelRide", "VirtualRide", "TrailRun"]:
            continue

        ranking[athlete] = ranking.get(athlete, 0) + distance_km

    ranking_sorted = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    result = {
        "last_update": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "ranking": [{"athlete": k, "distance_km": round(v, 1)} for k, v in ranking_sorted]
    }

    print("\n======== RESULTADO ========")
    print(json.dumps(result, indent=2))
    save_ranking(result)
    return result


def save_ranking(data):
    """Guarda el ranking generado en data/ranking.json"""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💾 Ranking guardado en {OUTPUT_FILE}")


if __name__ == "__main__":
    get_monthly_ranking()
