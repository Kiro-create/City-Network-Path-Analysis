import json
from flask import Flask, render_template, request, send_from_directory
from search_algorithms import ucs, greedy, a_star, bidirectional_ucs

ALGORITHMS = {
    "ucs": ("Uniform Cost Search", ucs),
    "greedy": ("Greedy Best-First Search", greedy),
    "astar": ("A* Search", a_star),
    "bidir": ("Bidirectional UCS", bidirectional_ucs)
}

app = Flask(__name__)

# Load places with node ids
with open("data/processed/places_with_nodes.json", encoding="utf-8") as f:
    places_data = json.load(f)

PLACES = places_data["places"]


@app.route("/")
def index():
    return render_template(
        "index.html",
        places=PLACES,
        preferred=None,
        results=None,
        cost=None,
        expanded=None
    )


@app.route("/graph.json")
def graph():
    return send_from_directory("data/processed", "road_graph.json")

@app.route("/find-path", methods=["POST"])
def find_path():
    start_name = request.form.get("start")
    goal_name = request.form.get("goal")
    mode = request.form.get("mode")          # manual | optimal | speed
    algo_key = request.form.get("algorithm") # used only if manual

    # map place names → node ids
    start_node = next(p["node_id"] for p in PLACES if p["name"] == start_name)
    goal_node = next(p["node_id"] for p in PLACES if p["name"] == goal_name)

    # -------------------------------------------------
    # Run ALL algorithms
    # -------------------------------------------------
    results = {}

    for key, (name, algo_func) in ALGORITHMS.items():
        path, cost, expanded = algo_func(start_node, goal_node)

        results[key] = {
            "name": name,
            "path": path,
            "cost": cost,
            "expanded": expanded
        }

    # -------------------------------------------------
    # Select algorithm based on MODE
    # -------------------------------------------------
    if mode == "manual":
        # User explicitly chooses algorithm
        preferred = results[algo_key]

    elif mode == "optimal":
        # Optimal cost, then fewest expanded nodes
        min_cost = min(r["cost"] for r in results.values())

        optimal_algos = [
            r for r in results.values()
            if abs(r["cost"] - min_cost) < 1e-6
        ]

        preferred = min(optimal_algos, key=lambda r: r["expanded"])

    elif mode == "speed":
        # Fewest expanded nodes only
        preferred = min(results.values(), key=lambda r: r["expanded"])

    else:
        # Safety fallback
        preferred = results["astar"]

    # -------------------------------------------------
    # Build path coordinates for map
    # -------------------------------------------------
    with open("data/processed/road_graph.json", encoding="utf-8") as f:
        graph = json.load(f)

    path_nodes = preferred["path"]
    path_coords = [
        [graph["nodes"][nid]["lat"], graph["nodes"][nid]["lng"]]
        for nid in path_nodes
    ]

    # -------------------------------------------------
    # Render result
    # -------------------------------------------------
    return render_template(
        "index.html",
        places=PLACES,
        path_coords=path_coords,
        results=results,
        preferred=preferred,
        cost=round(preferred["cost"], 2),
        expanded=preferred["expanded"],
        selected_start=start_name,
        selected_goal=goal_name,
        selected_mode=mode,
        selected_algorithm=algo_key
    )




if __name__ == "__main__":
    app.run(debug=True)
