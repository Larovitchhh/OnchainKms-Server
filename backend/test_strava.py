import requests

# ✅ Token actual válido
ACCESS_TOKEN = "eb6d80e6f9ee74ea61618bc69f1984cfc00fe0d8"
# ✅ ID numérico correcto del club OnchainKMS
CLUB_ID = "1814151"

url = f"https://www.strava.com/api/v3/clubs/{CLUB_ID}/activities"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

r = requests.get(url, headers=headers)

print("Status code:", r.status_code)
print("Response:")
print(r.json())
