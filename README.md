# City Network Path Analysis 🚦

An AI-powered pathfinding system that computes optimal and efficient routes across a real city road network using classical search algorithms.

## ✨ Features

* Real-world road network extracted from OpenStreetMap
* Multiple search algorithms:

  * Uniform Cost Search (UCS)
  * Greedy Best-First Search
  * A* Search
  * Bidirectional UCS
* Automatic algorithm selection based on:

  * **Optimality**
  * **Efficiency (expanded nodes)**
* Interactive map visualization using Leaflet
* Clean Flask-based web interface

## 🧠 Algorithms Overview

* **UCS**: Guarantees optimal paths but expands many nodes
* **Greedy**: Fast but not optimal
* **A***: Optimal with significantly fewer node expansions (recommended)
* **Bidirectional UCS**: Optimal, searches from start and goal simultaneously

## 🗂 Project Structure

* `app.py` – Flask application entry point
* `search_algorithms.py` – Search algorithm implementations
* `data/` – Raw and processed map data
* `scripts/` – Data preprocessing utilities
* `templates/` & `static/` – Frontend UI

## ▶️ How to Run

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## 🎓 Notes

This project was developed as part of an **Introduction to Artificial Intelligence** course, focusing on search algorithms, heuristics, and real-world graph modeling.
