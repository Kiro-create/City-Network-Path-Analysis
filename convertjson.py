import json
import math

ALLOWED_HIGHWAYS = {
    "motorway", "motorway_link",
    "primary", "secondary",
    "tertiary", "residential"
}

SPEEDS = {
    "motorway": 100,
    "motorway_link": 60,
    "primary": 60,
    "secondary": 50,
    "tertiary": 40,
    "residential": 30
}

with open("lines.geojson", "r", encoding="utf-8") as f:
    geo = json.load(f)

nodes = {}
edges = {}
coord_to_id = {}
node_id = 0

import math

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

def get_node_id(coord):
    global node_id

    if coord not in coord_to_id:
        coord_to_id[coord] = str(node_id)

        lon, lat = coord
        nodes[str(node_id)] = {
            "lat": lat,
            "lng": lon
        }
        edges[str(node_id)] = []

        node_id += 1

    return coord_to_id[coord]



for feature in geo["features"]:
    props = feature["properties"]
    geom = feature["geometry"]

    highway = props.get("highway")
    if highway not in ALLOWED_HIGHWAYS:
        continue

    coords = geom["coordinates"]
    oneway = props.get("oneway") == "yes"
    speed = SPEEDS[highway]
    name = props.get("name")
    osm_id = props.get("osm_id")

    for i in range(len(coords) - 1):
        a = coords[i]       # [lon, lat]
        b = coords[i + 1]   # [lon, lat]

        lon1, lat1 = a
        lon2, lat2 = b

        ida = get_node_id((lon1, lat1))
        idb = get_node_id((lon2, lat2))

        dist = haversine(lat1, lon1, lat2, lon2)  # km
        cost = (dist / speed) * 60                # minutes

        edge_data = {
            "to": idb,
            "cost": cost,
            "road_type": highway,
            "name": name,
            "osm_id": osm_id
        }


        edges[ida].append(edge_data)

        if not oneway:
            edges[idb].append({
                **edge_data,
                "to": ida
            })

with open("graph.json", "w", encoding="utf-8") as f:
    json.dump({"nodes": nodes, "edges": edges}, f, indent=2)

print("✅ Clean road graph created")
