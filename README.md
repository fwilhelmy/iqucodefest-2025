# iQuCodeFest 2025 - Super Quantum Party

This is the submission of the team QuantumETS1 for iQuCodeFest 2025!

To run the game, first install the virtual environment with all the env (see setup and installation section), then run the command
    ```
    python -m the_game```
    from the root repository

Quantum_mario_party.ipynb contient tout notre code directement en liens avec le calcul quantique

Voici la descriptions du fonctionnement:
Chaque joueur choisi leur noms, le premier joueur doit être la personne dans le group avec la meilleur théorie quantique.
Une fois fait, cliquez sur Play pour commencer.
Vous tombez alors dans un jeux similaire à super mario party, seulement version quantique :
- Vous roulez le dé quantique faisant une marche aléatoire quantique en cliquant sur Espace. (en phase 2, les distributions du dé change pour mieu tirer de cette distribution)
- Votre joueur se déplace dépendemment du nombre que vous avez obtenu en lançant le dé. 
- Si vous atterissez sur une case bleu, vous obtiendrez entre 1 à 4 partes quantiques dans votre inventaire.
- Si vous passer devant une étoile, vous gagnez une étoile dans votre inventaire.
- À chaque intersection, vous devez choisir le chemin sur lequel vous voulez allez. pour ce faire, utiliser les flèches sur votre clavier d'ordinateur et cliquer par la suite sur espace.
- à la fin de chaque tour, un mini-jeux apparait ! ce mini jeux permet de naviguer les différentes superposition de la carte (le graph avec noeuds). si l'état final mesuré est 01 ou 10, alors les "rivière" et les "portes" du niveau sont mesurer et ils "collapsent" vers seulement un chemin possible. Si l'état 11 est mesurer, la carte collapse sa superposition et le graph dirigé inverse sa direction. les joueurs doivent stratégiquement placer leur portes qu'ils ont collecter de sorte à obtenir l'état quantique qu'ils veulent. L'objectif étant de désavantager les autres d'obtenir une étoile tout en essayant de s'avantager.
- !!Présentement, il faut cliquer sur le bouton "measurement" avant de cliquer sur continuer si vous voulez que la carte change!!
- Attention ! Ajouter trop de gates rend le circuit inutilisable !
- Le gagnant est le joueur qui réussi à collecter le plus d'étoile et le plus de gates.

### future features

- implémentez des powerups -> ex: swap gate permet de s'intriquer avec un joueur et se teleporter à un moment choisi, 
- implémentez des minijeu quantique plus élaborer

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

   graph = build_graph_from_yaml("the_game/maps/new_map.yml")
   ```

If the YAML file omits pixel positions, coordinates are generated
automatically using NetworkX's spring layout.

---

You now have all the tools and resources needed to participate in the hackathon.
Good luck and have fun exploring quantum computing!
