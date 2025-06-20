"""Utilities to build game maps from YAML files."""
from __future__ import annotations

import os
from typing import Iterable, Mapping, Tuple

import networkx as nx
import yaml


_DEF_LAYOUT_SCALE = 500
_MIN_DIST = 60


def _spread_nodes(g: nx.DiGraph, min_dist: int = _MIN_DIST) -> None:
    """Adjust node positions to guarantee a minimum separation."""
    moved = True
    while moved:
        moved = False
        nodes = list(g.nodes())
        for i, n1 in enumerate(nodes):
            x1, y1 = g.nodes[n1]["pos"]
            for n2 in nodes[i + 1 :]:
                x2, y2 = g.nodes[n2]["pos"]
                dx, dy = x2 - x1, y2 - y1
                dist = (dx * dx + dy * dy) ** 0.5
                if dist and dist < min_dist:
                    shift = (min_dist - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    x1 -= ux * shift
                    y1 -= uy * shift
                    x2 += ux * shift
                    y2 += uy * shift
                    g.nodes[n1]["pos"] = (x1, y1)
                    g.nodes[n2]["pos"] = (x2, y2)
                    moved = True
    for n in g.nodes:
        x, y = g.nodes[n]["pos"]
        g.nodes[n]["pos"] = (int(x), int(y))


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

    _spread_nodes(g)

    return g
