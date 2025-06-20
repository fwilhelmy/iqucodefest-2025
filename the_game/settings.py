# Window & frame-rate constants; tweak once, propagate everywhere.
WIDTH, HEIGHT = 1100, 650
FPS           = 30

# Basic colour palette
BLACK = (0, 0, 0)
GREY  = (60, 60, 60)
GREEN = (25, 180, 40)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

# Paths to map thumbnails / backgrounds
# Map modules must be importable using their full package path. The previous
# values referred to a top-level ``maps`` package which does not exist, causing
# a crash when the Play button tries to load the selected map.  Prefix the
# module path with ``the_game`` so ``importlib`` can locate it correctly.
MAP_FILES   = ["maps.new_map",
               "maps.old_map"]  # second map not yet implemented
MAP_THUMBS  = ["resources/map1.png",
               "resources/map2.png"]
