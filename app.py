import json
from flask import Flask, render_template, request, send_from_directory
from Code import ucs, greedy, a_star, bidirectional_ucs

ALGORITHMS = {
    "ucs": ("Uniform Cost Search", ucs),
    "greedy": ("Greedy Best-First Search", greedy),
    "astar": ("A* Search", a_star),
    "bidir": ("Bidirectional UCS", bidirectional_ucs)
}

app = Flask(__name__)

with open("places_nodes.json", "r", encoding="utf-8") as f:
    places_data = json.load(f)

PLACES = places_data["places"]

@app.route("/")
def index():
    return render_template("index.html", places=PLACES)

@app.route("/graph.json")
def graph():
    return send_from_directory(".", "graph.json")

@app.route("/find-path", methods=["POST"])
def find_path():
    start_name = request.form.get("start")
    goal_name = request.form.get("goal")
    algo_key = request.form.get("algorithm")

    # map place names → node ids
    start_node = next(p["node_id"] for p in PLACES if p["name"] == start_name)
    goal_node = next(p["node_id"] for p in PLACES if p["name"] == goal_name)

    # select algorithm
    algo_name, algo_func = ALGORITHMS[algo_key]

    # run algorithm
    path_nodes, cost, expanded = algo_func(start_node, goal_node)

    # load graph for coordinates
    with open("graph.json", "r", encoding="utf-8") as f:
        graph = json.load(f)

    path_coords = [
        [graph["nodes"][nid]["lat"], graph["nodes"][nid]["lng"]]
        for nid in path_nodes
    ]

    return render_template(
        "index.html",
        places=PLACES,
        path_coords=path_coords,
        algo_name=algo_name,
        cost=round(cost, 2),
        expanded=expanded
    )



if __name__ == "__main__":
    app.run(debug=True)
