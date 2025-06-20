"""Utilities to build game maps from YAML files."""
from __future__ import annotations

import os
from typing import Iterable, Mapping, Tuple

import networkx as nx
import yaml


_DEF_LAYOUT_SCALE = 500


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
            attrs["pos"] = tuple(pos[name])
        g.add_node(name, **attrs)

    g.add_edges_from(edges)

    # Compute positions if none supplied
    if not pos:
        layout = nx.spring_layout(g, seed=0)
        for n, (x, y) in layout.items():
            g.nodes[n]["pos"] = (
                int(x * _DEF_LAYOUT_SCALE + _DEF_LAYOUT_SCALE),
                int(y * _DEF_LAYOUT_SCALE + _DEF_LAYOUT_SCALE / 2),
            )

    return g
