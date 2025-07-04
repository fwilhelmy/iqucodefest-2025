"""Example board data.

This module loads ``example_map.yml`` at runtime so the map can be edited
without touching the Python source.  If the YAML file is missing, the
fallback definitions below are used.
"""

from __future__ import annotations
import os
from typing import Iterable, Mapping, Tuple

import networkx as nx
import yaml

_DEF_LAYOUT_SCALE = 500
# Factor applied to all node positions loaded from YAML to allow easy
# adjustment of spacing without modifying the YAML file itself.
_POS_SCALE = 1.5

def build_graph_from_yaml(path: str) -> nx.DiGraph:
    """Create a directed graph from a YAML description.

    The YAML file should contain ``nodes`` and ``edges`` sections. ``pos`` is
    optional; if omitted, a spring layout is computed automatically.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    nodes: Mapping[str, Mapping] = data.get("nodes", {})
    edges: Iterable[Tuple[str, str]] = data.get("edges", [])
    pos   = data.get("pos")

    g = nx.DiGraph()
    for name, attrs in nodes.items():
        attrs = attrs or {}
        if pos and name in pos:
            x, y = pos[name]
            attrs["pos"] = (x * _POS_SCALE, y * _POS_SCALE)
        g.add_node(name, **attrs)

    g.add_edges_from(edges)

    # Compute positions if none supplied
    if not pos:
        layout = nx.spring_layout(g, seed=0)
        scale = _DEF_LAYOUT_SCALE * _POS_SCALE
        for n, (x, y) in layout.items():
            g.nodes[n]["pos"] = (
                int(x * scale + scale),
                int(y * scale + scale / 2),
            )

    return g

def build_graph() -> nx.DiGraph:
    """Return a fully attributed NetworkX graph ready for the GameScene."""
    yaml_path = os.path.join(os.path.dirname(__file__), "new_map.yml")
    return build_graph_from_yaml(yaml_path)
