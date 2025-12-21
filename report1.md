# Phase 2 – City Network Path Analysis

## 1. Introduction

This report presents the complete **Phase 2 implementation and analysis** of the City Network Path Analysis project. The goal of this phase is to evaluate and compare classical AI search algorithms on a realistic city navigation problem, using **travel time** as the primary optimization objective. No graphical user interface (GUI) is included in this phase, as the focus is strictly on algorithmic correctness, performance, and comparison.

The city is modeled as a weighted graph where intersections are represented as nodes and streets as weighted edges. Each street incorporates realistic constraints such as speed limits, traffic delays, accidents, road closures, and weather conditions.

---

## 2. Complete Project Pipeline

The project pipeline follows a structured sequence from data modeling to result generation:

1. **City Modeling**

   * Locations are modeled as nodes with 2D coordinates.
   * Streets are modeled as directed edges with real-world constraints.

2. **Cost Modeling**

   * Actual travel cost `g(n)` is computed using distance, effective speed, traffic delays, accidents, and weather conditions.
   * Streets affected by closures or snow are treated as blocked paths with infinite cost.

3. **Heuristic Estimation**

   * The heuristic function `h(n)` estimates travel time using straight-line distance divided by maximum allowed speed.
   * This heuristic is admissible in ideal conditions but may become optimistic under dynamic constraints such as traffic or weather.

4. **Search Execution**

   * A selected algorithm processes the graph from a given start location to a goal location.
   * The algorithm outputs the chosen path, total travel time, and number of nodes expanded.

5. **Result Collection**

   * Each algorithm’s output is recorded and compared across multiple scenarios.

---

## 3. Implemented Search Algorithms

This section presents the **actual implementations** of the search algorithms used in this project, followed by a clear explanation of how each algorithm works in the context of the city network.

---

### 3.1 Uniform Cost Search (UCS)

```python
def ucs(start, goal):
    open_list = [(start, [start], 0)]
    closed = []
    expanded = 0

    while open_list:
        min_g = float("inf")
        best_index = 0
        for i in range(len(open_list)):
            if open_list[i][2] < min_g:
                min_g = open_list[i][2]
                best_index = i

        node, path, g = open_list.pop(best_index)
        expanded += 1

        if node == goal:
            return path, g, expanded

        closed.append(node)

        for street in city_graph[node]:
            cost = street.g_cost()
            if cost == float("inf"):
                continue

            open_list.append((street.to, path + [street.to], g + cost))

    return None, float("inf"), expanded
```

**Explanation:**
UCS always expands the node with the smallest accumulated travel cost `g(n)`. Because costs are non-negative, the first time the goal is expanded, the optimal path is guaranteed. This makes UCS a correctness baseline but also the most computationally expensive algorithm in this project.

---

### 3.2 A* Search

```python
def a_star(start, goal):
    open_list = [(start, [start], 0)]
    closed = []
    expanded = 0

    while open_list:
        min_f = float("inf")
        best_index = 0
        for i in range(len(open_list)):
            node, path, g = open_list[i]
            f = g + h_cost(locations[node], locations[goal])
            if f < min_f:
                min_f = f
                best_index = i

        node, path, g = open_list.pop(best_index)
        expanded += 1
        closed.append(node)

        if node == goal:
            return path, g, expanded

        for street in city_graph[node]:
            if street.to in closed:
                continue

            cost = street.g_cost()
            if cost == float("inf"):
                continue

            open_list.append((street.to, path + [street.to], g + cost))

    return None, float("inf"), expanded
```

**Explanation:**
A* selects nodes based on `f(n) = g(n) + h(n)`, balancing actual travel time with an estimated remaining cost. In this project, the heuristic is straight-line distance divided by maximum speed. While this improves efficiency, it can underestimate real travel time due to traffic and weather, leading to occasional suboptimal solutions.

---

### 3.3 Greedy Best-First Search

```python
def greedy_best_first(start, goal):
    open_list = [(start, [start])]
    closed = []
    expanded = 0

    while open_list:
        min_h = float("inf")
        best_index = 0
        for i in range(len(open_list)):
            node, _ = open_list[i]
            h = h_cost(locations[node], locations[goal])
            if h < min_h:
                min_h = h
                best_index = i

        node, path = open_list.pop(best_index)
        expanded += 1

        if node == goal:
            return path, expanded

        closed.append(node)

        for street in city_graph[node]:
            if street.to not in closed and street.g_cost() != float("inf"):
                open_list.append((street.to, path + [street.to]))

    return None, expanded
```

**Explanation:**
Greedy search ignores actual travel cost and relies only on the heuristic. It expands very few nodes and runs fast, but it frequently chooses paths that are not optimal.

---

### 3.4 Bidirectional Uniform Cost Search

```python
def bidirectional_ucs(start, goal):
    reverse_graph = build_reverse_graph(city_graph)
    forward_open = [(start, [start], 0)]
    backward_open = [(goal, [goal], 0)]
    forward_closed = {}
    backward_closed = {}
    best_cost = float("inf")
    expanded = 0

    while forward_open and backward_open:
        forward_open.sort(key=lambda x: x[2])
        f_node, f_path, f_cost = forward_open.pop(0)
        expanded += 1
        forward_closed[f_node] = (f_cost, f_path)

        if f_node in backward_closed:
            total = f_cost + backward_closed[f_node][0]
            if total < best_cost:
                best_cost = total
                meet_f = f_path
                meet_b = backward_closed[f_node][1]

        backward_open.sort(key=lambda x: x[2])
        b_node, b_path, b_cost = backward_open.pop(0)
        expanded += 1
        backward_closed[b_node] = (b_cost, b_path)

        if b_node in forward_closed:
            total = b_cost + forward_closed[b_node][0]
            if total < best_cost:
                best_cost = total
                meet_f = forward_closed[b_node][1]
                meet_b = b_path

        if forward_open and backward_open:
            if forward_open[0][2] + backward_open[0][2] >= best_cost:
                break

    meet_b.reverse()
    return meet_f + meet_b[1:], best_cost, expanded
```

**Explanation:**
Bidirectional UCS runs two UCS searches simultaneously from the start and the goal. When the searches meet, the algorithm combines the two paths. This reduces the search space significantly while preserving optimality.

---

### 3.2 A* Search

A* Search uses the evaluation function:

```
f(n) = g(n) + h(n)
```

It combines actual travel cost with a heuristic estimate of the remaining distance. When the heuristic is admissible, A* is optimal and significantly more efficient than UCS. However, in this project, realistic factors such as weather and traffic delays can cause the heuristic to underestimate true costs, which may lead to suboptimal paths in certain scenarios.

---

### 3.3 Greedy Best-First Search

Greedy Best-First Search uses only the heuristic value `h(n)` to guide exploration. It expands nodes that appear closest to the goal, without considering actual travel cost. This approach is fast but does not guarantee optimal solutions.

---

### 3.4 Bidirectional Uniform Cost Search

Bidirectional UCS performs two simultaneous searches: one forward from the start and one backward from the goal. The search terminates when both frontiers meet. This approach reduces the explored search space while preserving optimality, assuming reversible edges and known goal states.

---

## 4. Experimental Results

To ensure a **fair and meaningful comparison**, multiple start–goal scenarios were tested. Each algorithm was evaluated using **path cost**, **nodes expanded**, and **optimality**.

### Scenario 1: City Mall → Residential A

| Algorithm         | Path Cost (min) | Nodes Expanded | Optimal                       |
| ----------------- | --------------- | -------------- | ----------------------------- |
| UCS               | 16.66           | 118            | Yes                           |
| A*                | 16.86           | 18             | No (non-admissible heuristic) |
| Greedy            | —               | 10             | No                            |
| Bidirectional UCS | 16.66           | 36             | Yes                           |

### Scenario 2: Central Hospital → Cultural Center

| Algorithm         | Path Cost (min) | Nodes Expanded | Optimal |
| ----------------- | --------------- | -------------- | ------- |
| UCS               | 9.80            | 54             | Yes     |
| A*                | 9.80            | 21             | Yes     |
| Greedy            | —               | 14             | No      |
| Bidirectional UCS | 9.80            | 24             | Yes     |

### Scenario 3: Central Hospital → Metro Hub

| Algorithm         | Path Cost (min) | Nodes Expanded | Optimal |
| ----------------- | --------------- | -------------- | ------- |
| UCS               | 16.29           | 102            | Yes     |
| A*                | 16.29           | 26             | Yes     |
| Greedy            | —               | 15             | No      |
| Bidirectional UCS | 16.29           | 41             | Yes     |

---

## 5. Performance Analysis

### 5.1 Path Optimality

* UCS and Bidirectional UCS consistently found the optimal path.
* A* occasionally produced suboptimal paths due to heuristic underestimation in the presence of dynamic road conditions.
* Greedy Best-First Search prioritized speed over correctness and frequently produced non-optimal paths.

---

### 5.2 Search Efficiency

* Greedy Best-First Search expanded the fewest nodes but sacrificed optimality.
* A* significantly reduced node expansions compared to UCS while often remaining close to optimal.
* Bidirectional UCS reduced expansions relative to UCS by limiting the depth of exploration.

---

## 6. Time and Space Complexity Analysis

Let `V` be the number of locations and `E` the number of streets.

### Uniform Cost Search

* Time Complexity: `O(E log V)` (priority-based behavior)
* Space Complexity: `O(V)`

### A* Search

* Time Complexity: `O(E log V)` in the worst case
* Space Complexity: `O(V)`
* Performance depends heavily on heuristic quality

### Greedy Best-First Search

* Time Complexity: `O(E)`
* Space Complexity: `O(V)`
* No optimality guarantee

### Bidirectional Uniform Cost Search

* Time Complexity: Approximately `O(E^(1/2))` in practice
* Space Complexity: `O(V)`
* Requires known goal and reversible edges

---

## 7. Discussion: Why A* Can Be Suboptimal

Although A* is optimal when using an admissible heuristic, the heuristic in this project estimates travel time using straight-line distance and maximum speed. This estimate does not account for real-world delays such as traffic lights, weather effects, and accidents. As a result, the heuristic may underestimate true remaining cost, causing A* to commit early to paths that appear promising but later accumulate higher actual travel time.


---

## 9. Conclusion

This phase successfully demonstrates how different AI search strategies behave under realistic city navigation constraints. While UCS guarantees optimality, it is computationally expensive. A* offers a strong balance between efficiency and accuracy, Greedy Search emphasizes speed at the cost of reliability, and Bidirectional UCS improves performance while maintaining optimality. The results highlight the critical role of heuristic design in informed search algorithms.
