# iQuCodeFest 2025

This is the submission of the team QuantumETS1 for iQuCodeFest 2025!

To run the game, first install the virtual environment with all the env, then run the command
    ```bash
    python -m the_game
    ```
    from the root repository

#### Quantum Board Game Challenge Summary

---

## Setup and Installation

To set up your environment:

1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd iQuCodeFest_2025
    ```
2. **(Recommended) Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install required packages:**
    ```bash
    pip install -r requirements.txt
    ```


---

## Building New Game Maps

The Pygame prototype stores each board as a directed graph. You can describe
new maps using a compact YAML file and load them with
`build_graph_from_yaml`.

1. Create a YAML file with `nodes` and `edges` (see
   `the_game/maps/example_map.yml` for a full example).
2. Load it in your code:

   ```python
   from the_game.maps.yaml_map import build_graph_from_yaml

   graph = build_graph_from_yaml("the_game/maps/example_map.yml")
   ```

If the YAML file omits pixel positions, coordinates are generated
automatically using NetworkX's spring layout.

---

You now have all the tools and resources needed to participate in the hackathon.
Good luck and have fun exploring quantum computing!
