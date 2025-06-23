# Super Quantum Party

![screenshot](resources/superquantumparty.png)

## 1. Overview

Super Quantum Party is the winning submission from the **Quantum ETS1** team (Felix Wilhelmy, Charles A. Bédard, Gabriel Lemay, Guy-Philippe Nadon) at **iQuCodeFest 2025**. The 30‑hour on‑site hackathon took place 19–20&nbsp;June&nbsp;2025 at Polytechnique Montréal and was organized by Polytechnique Montréal, Institut quantique / Université de Sherbrooke, University of Calgary, École de technologie supérieure (ÉTS), Quantum City and PINQ².

The main challenge was to redesign a classic board game by integrating quantum concepts and deliver a Python prototype with playable rules. This repository contains our prototype built with Python 3.11, Qiskit/IBM Quantum (via PINQ² credentials) and the standard SciPy stack.

## 2. Game concept & quantum mechanics

* Pygame board built from a YAML‑described directed graph
* Quantum dice powered by Qiskit implementing a quantum walk
* Collect quantum gates and stars as you traverse the board
* Gate minigame lets players apply operations; measurement outcomes alter the board's edges
* After the last turn, a results scene ranks players by stars and collected gates

## 3. Installation & quick‑start

### Conda
```bash
conda create -n quantum-party python=3.11
conda activate quantum-party
pip install -r requirements.txt
```

### pip only
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the game
From the repository root:
```bash
python -m the_game
```

## 4. Usage examples

### Build your own map
```python
from the_game.maps.yaml_map import build_graph_from_yaml
my_map = build_graph_from_yaml("the_game/maps/new_map.yml")
```

### Launching the prototype
```bash
$ python -m the_game
>>> switched to MenuScene
```

## 5. Contributing

We welcome pull requests for bug fixes, docs and new board ideas. Fork the repo, create a feature branch and open a PR.

## 6. License & acknowledgments

This project is released under the [MIT License](LICENSE). We thank the iQuCodeFest 2025 organizers and backers—Polytechnique Montréal, Institut quantique / Université de Sherbrooke, University of Calgary, École de technologie supérieure (ÉTS), Quantum City and PINQ²—for making the event possible.

---

### About Quantum ÉTS

Quantum ÉTS is a growing community of students exploring quantum information science. [Learn more](https://TODO.example.com).
