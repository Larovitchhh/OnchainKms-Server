import os
import requests

ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

print("🔑 Using token:", ACCESS_TOKEN)

url = "https://www.strava.com/api/v3/athlete/activities?per_page=5"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print("Response:", response.json())
