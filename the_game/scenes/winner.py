import pygame, sys
from settings import WIDTH, HEIGHT, WHITE, BLACK
from core.scene import Scene
from ui.widgets import Button

class WinnerScene(Scene):
    def __init__(self, manager, players):
        super().__init__(manager)
        # Sort players by stars desc, then by gate count desc
        self.players = sorted(
            players,
            key=lambda p: (-p.stars, -sum(p.gates.values()))
        )
        self.font_big = pygame.font.SysFont(None, 48)
        self.font = pygame.font.SysFont(None, 32)
        self.button = Button("Menu", (WIDTH//2, HEIGHT - 60))

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            from scenes.menu import MenuScene
            self.manager.go_to(MenuScene(self.manager))
        if self.button.handle_event(e):
            from scenes.menu import MenuScene
            self.manager.go_to(MenuScene(self.manager))
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    def update(self, dt):
        pass

    def draw(self, s):
        s.fill(WHITE)
        title = self.font_big.render("Results", True, BLACK)
        s.blit(title, title.get_rect(center=(WIDTH//2, 80)))
        for i, p in enumerate(self.players):
            text = f"{i+1}. {p.name} - {p.stars}\u2605 - {sum(p.gates.values())} gates"
            img = self.font.render(text, True, BLACK)
            s.blit(img, (WIDTH//2 - img.get_width()//2, 150 + i*40))
        self.button.draw(s)
