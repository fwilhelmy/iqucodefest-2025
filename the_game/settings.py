# Window & frame-rate constants; tweak once, propagate everywhere.
import os

WIDTH, HEIGHT = 1100, 650
FPS = 60

# Basic colour palette
BLACK = (0, 0, 0)
GREY = (60, 60, 60)
GREEN = (25, 180, 40)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

# Base path for bundled images and other assets
BASE_DIR = os.path.dirname(__file__)
RES_DIR = os.path.join(BASE_DIR, "resources")

# Paths to map thumbnails / backgrounds
# Game scenes load these maps dynamically using ``importlib``.  Because the
# game is usually launched by running ``the_game/main.py`` directly (without
# installing the package), the directory ``the_game`` itself is placed on
# ``sys.path``.  Map modules therefore live under the top-level ``maps``
# package rather than ``the_game.maps``.
MAP_FILES = ["maps.example_map", "maps.example_map"]  # second map not yet implemented
MAP_THUMBS = [os.path.join(RES_DIR, "map1.png"), os.path.join(RES_DIR, "map2.png")]
