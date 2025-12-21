import json
import math

# -------------------------
# Distance function
# -------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# -------------------------
# Load places
# -------------------------
with open("places.json", "r", encoding="utf-8") as f:
    places_data = json.load(f)

places = places_data["places"]


# -------------------------
# Load graph nodes
# -------------------------
with open("graph.json", "r", encoding="utf-8") as f:
    graph_data = json.load(f)

nodes = graph_data["nodes"]


# -------------------------
# Snap each place to nearest node
# -------------------------
snapped_places = []

for place in places:
    place_lat = place["lat"]
    place_lon = place["lon"]

    closest_node = None
    min_distance = float("inf")

    for node_id, node in nodes.items():
        node_lat = node["lat"]
        node_lon = node["lng"]

        d = haversine(place_lat, place_lon, node_lat, node_lon)

        if d < min_distance:
            min_distance = d
            closest_node = node_id

    snapped_places.append({
        "id": place["id"],
        "name": place["name"],
        "type": place["type"],
        "lat": place_lat,
        "lon": place_lon,
        "node_id": closest_node
    })


# -------------------------
# Save result
# -------------------------
with open("places_nodes.json", "w", encoding="utf-8") as f:
    json.dump({"places": snapped_places}, f, indent=2)

print(f"✅ Snapped {len(snapped_places)} places to nearest road nodes")
