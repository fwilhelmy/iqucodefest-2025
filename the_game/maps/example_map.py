"""
Human-friendly definition of one board.

Editing rule of thumb:
• One dictionary entry  →  one node
• One tuple in EDGES    →  one directed arrow
• POS keeps the on-screen coordinates; use any pixels you like.
"""

import networkx as nx

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
    g = nx.DiGraph()
    for n, data in NODES.items():
        g.add_node(n, **data, pos=POS[n])
    g.add_edges_from(EDGES)
    return g
