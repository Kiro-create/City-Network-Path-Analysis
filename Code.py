import math
import json

# Open and load the places.json file
with open("places.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Dictionary to store: name -> (lat, lon)
locations = {}

# Loop through the list of places
for place in data["places"]:
    name = place["name"]
    lat = place["lat"]
    lon = place["lon"]

    locations[name] = (lat, lon)

# (Optional) print to check
#print(locations)

def get_start_goal_nodes(start, goal):
    with open("places_nodes.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    start_node = None
    goal_node = None

    for place in data["places"]:
        if place["name"] == start:
            start_node = place["node_id"]

        if place["name"] == goal:
            goal_node = place["node_id"]

    return start_node, goal_node

# ----------------------------------
# Configuration (easy to tweak)
# ----------------------------------
INTERSECTION_PENALTY = 0.15  # ~5 sec

ROAD_TYPE_FACTOR = {
    "motorway": 1.0,
    "motorway_link": 1.05,
    "primary": 1.1,
    "secondary": 1.2,
    "tertiary": 1.25,
    "residential": 1.3
}

DEFAULT_ROAD_FACTOR = 1.3


# ----------------------------------
# Uniform Cost Search (Realistic)
# ----------------------------------
def ucs(start_node, goal_node):
    with open("graph.json", "r", encoding="utf-8") as f:
        graph = json.load(f)

    edges = graph["edges"]

    open_list = [(0, start_node, [start_node])]
    closed_list = {}

    expanded = 0

    while open_list:
        open_list.sort(key=lambda x: x[0])
        current_cost, current_node, path = open_list.pop(0)

        if current_node in closed_list and closed_list[current_node] <= current_cost:
            continue

        closed_list[current_node] = current_cost
        expanded += 1

        # Goal reached
        if current_node == goal_node:
            return path, current_cost, expanded

        # Expand neighbors
        for edge in edges.get(current_node, []):
            next_node = edge["to"]

            # --- Option B: road type realism ---
            road_type = edge.get("road_type")
            factor = ROAD_TYPE_FACTOR.get(road_type, DEFAULT_ROAD_FACTOR)

            adjusted_edge_cost = edge["cost"] * factor

            # --- Option A: intersection delay ---
            new_cost = current_cost + adjusted_edge_cost + INTERSECTION_PENALTY

            new_path = path + [next_node]
            open_list.append((new_cost, next_node, new_path))

    return None, float("inf"), expanded

# ----------------------------------
# A* Search
# ----------------------------------
def a_star(start_node, goal_node):
    with open("graph.json", "r", encoding="utf-8") as f:
        graph = json.load(f)

    edges = graph["edges"]
    nodes = graph["nodes"]

    goal_lat = nodes[goal_node]["lat"]
    goal_lon = nodes[goal_node]["lng"]

    # OPEN: (f, g, node, path)
    open_list = [(0, 0, start_node, [start_node])]

    # CLOSED: node_id -> best g-cost
    closed_list = {}

    expanded = 0

    while open_list:
        open_list.sort(key=lambda x: x[0])
        _, g_cost, current_node, path = open_list.pop(0)

        if current_node in closed_list and closed_list[current_node] <= g_cost:
            continue

        closed_list[current_node] = g_cost
        expanded += 1

        # Goal reached
        if current_node == goal_node:
            return path, g_cost, expanded

        # Expand neighbors
        for edge in edges.get(current_node, []):
            next_node = edge["to"]

            # --- Realistic edge cost ---
            road_type = edge.get("road_type")
            factor = ROAD_TYPE_FACTOR.get(road_type, DEFAULT_ROAD_FACTOR)
            step_cost = edge["cost"] * factor + INTERSECTION_PENALTY
            new_g = g_cost + step_cost

            # --- Heuristic ---
            lat = nodes[next_node]["lat"]
            lon = nodes[next_node]["lng"]
            h = haversine(lat, lon, goal_lat, goal_lon)

            new_f = new_g + h
            new_path = path + [next_node]

            open_list.append((new_f, new_g, next_node, new_path))

    return None, float("inf"), expanded


# ----------------------------------
# Heuristic: straight-line distance
# ----------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ----------------------------------
# Greedy Best-First Search
# ----------------------------------
def greedy(start_node, goal_node):
    with open("graph.json", "r", encoding="utf-8") as f:
        graph = json.load(f)

    edges = graph["edges"]
    nodes = graph["nodes"]

    goal_lat = nodes[goal_node]["lat"]
    goal_lon = nodes[goal_node]["lng"]

    # OPEN: (heuristic, cost_so_far, node, path)
    open_list = [(0, 0, start_node, [start_node])]
    closed_set = set()

    expanded = 0

    while open_list:
        open_list.sort(key=lambda x: x[0])
        h, current_cost, current_node, path = open_list.pop(0)

        if current_node in closed_set:
            continue

        closed_set.add(current_node)
        expanded += 1

        if current_node == goal_node:
            return path, current_cost, expanded

        for edge in edges.get(current_node, []):
            next_node = edge["to"]

            if next_node in closed_set:
                continue

            # --- Realistic cost (same as UCS) ---
            road_type = edge.get("road_type")
            factor = ROAD_TYPE_FACTOR.get(road_type, DEFAULT_ROAD_FACTOR)
            edge_cost = edge["cost"] * factor + INTERSECTION_PENALTY
            new_cost = current_cost + edge_cost

            # --- Heuristic ONLY drives priority ---
            lat = nodes[next_node]["lat"]
            lon = nodes[next_node]["lng"]
            heuristic = haversine(lat, lon, goal_lat, goal_lon)

            open_list.append((heuristic, new_cost, next_node, path + [next_node]))

    return None, float("inf"), expanded

# ----------------------------------
# Build reverse graph
# ----------------------------------
def build_reverse_edges(edges):
    reverse = {}

    for u, edge_list in edges.items():
        for edge in edge_list:
            v = edge["to"]
            reverse.setdefault(v, []).append({
                "to": u,
                "cost": edge["cost"],
                "road_type": edge.get("road_type")
            })

    return reverse


# ----------------------------------
# Bidirectional UCS
# ----------------------------------
def bidirectional_ucs(start_node, goal_node):
    import json

    # ---------------- LOAD GRAPH ----------------
    with open("graph.json", "r", encoding="utf-8") as f:
        graph = json.load(f)

    edges = graph["edges"]
    reverse_edges = build_reverse_edges(edges)

    # ---------------- OPEN LISTS ----------------
    # (cost, node)
    open_fwd = [(0, start_node)]
    open_bwd = [(0, goal_node)]

    # ---------------- CLOSED LISTS ----------------
    # node -> best cost
    closed_fwd = {start_node: 0}
    closed_bwd = {goal_node: 0}

    # ---------------- PARENT POINTERS ----------------
    parent_fwd = {start_node: None}
    parent_bwd = {goal_node: None}

    # ---------------- TERMINATION TRACKING ----------------
    best_cost = float("inf")   # 🔴 FIX: track best meeting cost
    meeting_node = None

    expanded = 0

    # ---------------- MAIN LOOP ----------------
    while open_fwd and open_bwd:

        # 🔴 FIX 1: correct UCS termination condition
        open_fwd.sort(key=lambda x: x[0])
        open_bwd.sort(key=lambda x: x[0])

        if open_fwd[0][0] + open_bwd[0][0] >= best_cost:
            break

        # 🔴 FIX 2: expand the cheaper frontier
        if open_fwd[0][0] <= open_bwd[0][0]:
            # -------- FORWARD EXPANSION --------
            cost_f, node_f = open_fwd.pop(0)
            expanded += 1

            # Skip dominated entries
            if cost_f > closed_fwd.get(node_f, float("inf")):
                continue

            # 🔴 FIX 3: meeting does NOT terminate immediately
            if node_f in closed_bwd:
                total = cost_f + closed_bwd[node_f]
                if total < best_cost:
                    best_cost = total
                    meeting_node = node_f

            # Expand neighbors
            for edge in edges.get(node_f, []):
                nxt = edge["to"]
                new_cost = cost_f + edge["cost"]

                if new_cost < closed_fwd.get(nxt, float("inf")):
                    closed_fwd[nxt] = new_cost
                    parent_fwd[nxt] = node_f
                    open_fwd.append((new_cost, nxt))

        else:
            # -------- BACKWARD EXPANSION --------
            cost_b, node_b = open_bwd.pop(0)
            expanded += 1

            if cost_b > closed_bwd.get(node_b, float("inf")):
                continue

            if node_b in closed_fwd:
                total = cost_b + closed_fwd[node_b]
                if total < best_cost:
                    best_cost = total
                    meeting_node = node_b

            for edge in reverse_edges.get(node_b, []):
                nxt = edge["to"]
                new_cost = cost_b + edge["cost"]

                if new_cost < closed_bwd.get(nxt, float("inf")):
                    closed_bwd[nxt] = new_cost
                    parent_bwd[nxt] = node_b
                    open_bwd.append((new_cost, nxt))

    # ---------------- NO SOLUTION ----------------
    if meeting_node is None:
        return None, float("inf"), expanded

    # ---------------- PATH RECONSTRUCTION ----------------
    # 🔴 FIX 4: reconstruct path AFTER search finishes

    path = []

    # start → meeting
    n = meeting_node
    while n is not None:
        path.append(n)
        n = parent_fwd[n]
    path.reverse()

    # meeting → goal (skip meeting node)
    n = parent_bwd.get(meeting_node)
    while n is not None:
        path.append(n)
        n = parent_bwd[n]

    return path, best_cost, expanded


def main():
    print("===== City Network Path Analysis =====\n")

    print("Available Locations:")
    for loc in locations:
        print("-", loc)

    print("\nEnter start and goal locations exactly as shown above.\n")

    start = input("Start location: ").strip()
    goal = input("Goal location: ").strip()

    print("\n====================================")
    print(f"Start: {start}")
    print(f"Goal : {goal}")
    print("====================================\n")

    start_id, goal_id = get_start_goal_nodes(start, goal)

    # ---------- UCS ----------
    path, cost, expanded = ucs(start_id, goal_id)
    print("Algorithm: Uniform Cost Search (UCS)")
    if path is None:
        print("Path: No path found")
    else:
        print("Path:", " -> ".join(path))
    print(f"Total Travel Time: {cost:.2f} minutes")
    print(f"Nodes Expanded: {expanded}\n")

    # ---------- Greedy ----------
    path, cost, expanded = greedy(start_id, goal_id)
    print("Algorithm: Greedy Best-First Search")
    if path is None:
        print("Path: No path found")
    else:
        print("Path:", " -> ".join(path))
    print("Total Travel Time:", round(cost, 2), "minutes")
    print(f"Nodes Expanded: {expanded}\n")

    # ---------- A* ----------
    path, cost, expanded = a_star(start_id, goal_id)
    print("Algorithm: A* Search")
    if path is None:
        print("Path: No path found")
    else:
        print("Path:", " -> ".join(path))
    print(f"Total Travel Time: {cost:.2f} minutes")
    print(f"Nodes Expanded: {expanded}\n")


    # ---------- Bidirectional UCS ----------
    path, cost, expanded = bidirectional_ucs(start_id, goal_id)
    print("Algorithm: Bidirectional Uniform Cost Search")
    if path is None:
        print("Path: No path found")
    else:
        print("Path:", " -> ".join(path))
    print(f"Total Travel Time: {cost:.2f} minutes")
    print(f"Nodes Expanded: {expanded}\n")

    print("===== End of Analysis =====")


if __name__ == "__main__":
    main()