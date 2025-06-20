"""Example board data.

This module loads ``example_map.yml`` at runtime so the map can be edited
without touching the Python source.  If the YAML file is missing, the
fallback definitions below are used.
"""

from __future__ import annotations

import os

import networkx as nx

from .yaml_map import build_graph_from_yaml

# ── 1)  Nodes ──────────────────────────────────────────────────────────
NODES = {
    "A": {"type": 1, "value": 2},                 # blue  (gives 2 gates)
    "B": {"type": 1, "value": 4},                 # blue
    "C": {"type": 2, "value": 1},                 # red   (takes 1 gate)
    "D": {"type": 3, "trigger": ["01", "11"]},    # yellow (toggle)
    "E": {"type": 4},                             # gold  (“star” node)
}

# ── 2)  Directed edges (arrows) ────────────────────────────────────────
EDGES = [
    ("A", "B"),
    ("B", "C"),
    ("A", "D"),
    ("D", "E"),
    ("E", "C"),
]

# ── 3)  Pixel positions (for drawing) ──────────────────────────────────
POS = {
    "A": (150, 120),
    "B": (380, 120),
    "C": (610, 260),
    "D": (380, 260),
    "E": (380, 420),
}


def build_graph() -> nx.DiGraph:
    """Return a fully attributed NetworkX graph ready for the GameScene."""
    yaml_path = os.path.join(os.path.dirname(__file__), "example_map.yml")
    if os.path.exists(yaml_path):
        return build_graph_from_yaml(yaml_path)

    g = nx.DiGraph()
    for n, data in NODES.items():
        g.add_node(n, **data, pos=POS[n])
    g.add_edges_from(EDGES)
    return g
