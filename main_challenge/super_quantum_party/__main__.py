import pygame, sys
from super_quantum_party.settings import WIDTH, HEIGHT, FPS
from super_quantum_party.ui.widgets import init_fonts
from super_quantum_party.core.scene import SceneManager
from super_quantum_party.scenes.menu import MenuScene

# ─── initialise Pygame & fonts ─────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()
pygame.display.set_caption("Super Quantum Party")

# Fonts must be created *after* pygame.init()
FONT_L = pygame.font.SysFont(None, 72)
FONT_M = pygame.font.SysFont(None, 32)
FONT_S = pygame.font.SysFont(None, 24)
init_fonts(FONT_L, FONT_M, FONT_S)          # give them to the widgets

# ─── boot the first scene ──────────────────────────────────────────────
manager = SceneManager(MenuScene(None))     # create scene without manager
manager.scene.manager = manager             # then patch back-reference

# ─── main loop ─────────────────────────────────────────────────────────
while True:
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        manager.handle_event(event)

    manager.update(dt)
    manager.draw(screen)
    pygame.display.flip()
