import pygame, sys
from super_quantum_party.settings import WIDTH, HEIGHT, WHITE, BLACK, YELLOW
from super_quantum_party.core.scene import Scene
from super_quantum_party.ui.widgets import Button

class WinnerScene(Scene):
    def __init__(self, manager, players):
        super().__init__(manager)
        # Sort players by stars desc, then by gate count desc
        self.players = sorted(
            players,
            key=lambda p: (-p.stars, -sum(p.gates.values()))
        )
        comic = pygame.font.match_font("comicsansms")
        self.font_big = pygame.font.Font(comic or pygame.font.get_default_font(), 64)
        self.font = pygame.font.Font(comic or pygame.font.get_default_font(), 36)
        self.button = Button("Menu", (WIDTH//2, HEIGHT - 60))

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            from super_quantum_party.scenes.menu import MenuScene
            self.manager.go_to(MenuScene(self.manager))
        if self.button.handle_event(e):
            from super_quantum_party.scenes.menu import MenuScene
            self.manager.go_to(MenuScene(self.manager))
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    def update(self, dt):
        pass

    def draw(self, s):
        s.fill(WHITE)
        title = self.font_big.render("Results", True, YELLOW)
        s.blit(title, title.get_rect(center=(WIDTH // 2, 80)))
        for i, p in enumerate(self.players):
            text = f"{i+1}. {p.name} - {p.stars}* - {sum(p.gates.values())} gates"
            img = self.font.render(text, True, BLACK)
            pos = (WIDTH // 2 - img.get_width() // 2, 150 + i * 50)
            if i == 0:
                bg = img.get_rect(topleft=pos).inflate(20, 10)
                pygame.draw.rect(s, YELLOW, bg)
            s.blit(img, pos)
        self.button.draw(s)
