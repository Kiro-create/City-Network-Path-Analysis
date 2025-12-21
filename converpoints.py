import json

INPUT_FILE = "points.geojson"
OUTPUT_FILE = "places.json"

places = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    geo = json.load(f)

for feature in geo["features"]:
    props = feature.get("properties", {})
    geom = feature.get("geometry", {})

    if geom.get("type") != "Point":
        continue

    coords = geom.get("coordinates")
    if not coords:
        continue

    lon, lat = coords
    name = props.get("name")

    # Skip unnamed points (unless it's a city)
    if not name and props.get("place") != "city":
        continue

    place = {
        "id": props.get("osm_id"),
        "name": name,
        "type": props.get("place")
                or props.get("amenity")
                or props.get("highway")
                or "unknown",
        "lat": lat,
        "lon": lon
    }

    places.append(place)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"places": places}, f, indent=2)

print(f"✅ Saved {len(places)} places to {OUTPUT_FILE}")
