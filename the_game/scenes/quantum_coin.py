import pygame, sys
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from settings import WIDTH, HEIGHT, WHITE, BLACK
from core.scene import Scene, SceneManager
from ui.widgets import Button

class QuantumCoinScene(Scene):
    """Simple coin flip using Qiskit AerSimulator."""
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont(None, 48)
        self.result = None
        self.button = Button("Flip", (WIDTH//2, HEIGHT//2))

    def _flip_coin(self):
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        sim = AerSimulator()
        counts = sim.run(qc).result().get_counts()
        # get most probable bit (since only one shot)
        self.result = max(counts, key=counts.get)

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()
        if self.button.handle_event(e):
            self._flip_coin()
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    def update(self, dt):
        pass

    def draw(self, s):
        s.fill(WHITE)
        txt = self.font.render("Quantum Coin Toss", True, BLACK)
        s.blit(txt, txt.get_rect(center=(WIDTH//2, 80)))
        self.button.draw(s)
        if self.result is not None:
            res_txt = self.font.render(f"Result: {self.result}", True, BLACK)
            s.blit(res_txt, res_txt.get_rect(center=(WIDTH//2, HEIGHT//2 + 80)))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    from ui.widgets import init_fonts
    font_l = pygame.font.SysFont(None, 72)
    font_m = pygame.font.SysFont(None, 32)
    font_s = pygame.font.SysFont(None, 24)
    init_fonts(font_l, font_m, font_s)
    manager = SceneManager(QuantumCoinScene(None))
    manager.scene.manager = manager
    while True:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            manager.handle_event(event)
        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()
