import requests
import pandas as pd
import time

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# -----------------------------
# Major cities per state (expandable)
# -----------------------------
INDIA_LOCATIONS = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur"],
    "Assam": ["Guwahati", "Dibrugarh"],
    "Bihar": ["Patna", "Gaya"],
    "Chhattisgarh": ["Raipur", "Bilaspur"],
    "Delhi": ["New Delhi"],
    "Goa": ["Panaji", "Margao"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "Haryana": ["Gurgaon", "Faridabad"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode"],
    "Madhya Pradesh": ["Bhopal", "Indore"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "Odisha": ["Bhubaneswar", "Cuttack"],
    "Punjab": ["Chandigarh", "Ludhiana"],
    "Rajasthan": ["Jaipur", "Jodhpur"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Telangana": ["Hyderabad"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Noida"],
    "West Bengal": ["Kolkata", "Howrah"]
}

rows = []
hospital_id = 1

def fetch_hospitals(city):
    query = f"""
    [out:json][timeout:25];
    area["name"="{city}"]->.searchArea;
    (
      node["amenity"="hospital"](area.searchArea);
      way["amenity"="hospital"](area.searchArea);
      relation["amenity"="hospital"](area.searchArea);
    );
    out center tags;
    """
    response = requests.post(OVERPASS_URL, data=query)
    return response.json().get("elements", [])

# -----------------------------
# MAIN LOOP
# -----------------------------
for state, cities in INDIA_LOCATIONS.items():
    for city in cities:
        print(f"Fetching hospitals for {city}, {state}")
        try:
            results = fetch_hospitals(city)
        except Exception as e:
            print("Error:", e)
            continue

        for place in results:
            tags = place.get("tags", {})
            name = tags.get("name")
            if not name:
                continue

            lat = place.get("lat") or place.get("center", {}).get("lat")
            lon = place.get("lon") or place.get("center", {}).get("lon")
            if not lat or not lon:
                continue

            rows.append({
                "hospital_id": hospital_id,
                "hospital_name": name,
                "state": state,
                "district": city,
                "city": city,
                "latitude": lat,
                "longitude": lon
            })
            hospital_id += 1

        time.sleep(3)  # respectful delay

# -----------------------------
# SAVE DATA
# -----------------------------
df = pd.DataFrame(rows)
df.drop_duplicates(subset=["hospital_name", "city"], inplace=True)

df.to_csv("data/real_india_hospitals_raw.csv", index=False)

print("Total real hospitals collected:", len(df))
