import pygame, sys
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector

import matplotlib.pyplot as plt

from settings import WIDTH, HEIGHT, WHITE, BLACK
from the_game.core.scene import Scene, SceneManager

class StatevectorDemo(Scene):
    """Simple interactive demo manipulating a single-qubit state."""
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont(None, 36)
        self.state = Statevector([1, 0])
        self.image = None
        self._update_image()
        self.instructions = self.font.render(
            "Press H/X/Y/Z to apply gate, ESC to exit", True, BLACK)

    def _update_image(self):
        px = float(self.state.expectation_value('X').real)
        py = float(self.state.expectation_value('Y').real)
        pz = float(self.state.expectation_value('Z').real)
        fig = plot_bloch_vector([px, py, pz])
        fig.savefig("/tmp/state.png")
        plt.close(fig)
        self.image = pygame.image.load("/tmp/state.png").convert_alpha()

    def _apply(self, gate):
        qc = QuantumCircuit(1)
        getattr(qc, gate.lower())(0)
        self.state = self.state.evolve(qc)
        self._update_image()

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            elif e.key == pygame.K_h: self._apply('h')
            elif e.key == pygame.K_x: self._apply('x')
            elif e.key == pygame.K_y: self._apply('y')
            elif e.key == pygame.K_z: self._apply('z')
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    def update(self, dt):
        pass

    def draw(self, s):
        s.fill(WHITE)
        title = self.font.render("Statevector Demo", True, BLACK)
        s.blit(title, title.get_rect(center=(WIDTH//2, 40)))
        s.blit(self.instructions, self.instructions.get_rect(center=(WIDTH//2, HEIGHT-40)))
        if self.image:
            img = pygame.transform.smoothscale(self.image, (300, 300))
            rect = img.get_rect(center=(WIDTH//2, HEIGHT//2))
            s.blit(img, rect)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    from ui.widgets import init_fonts
    font_l = pygame.font.SysFont(None, 72)
    font_m = pygame.font.SysFont(None, 32)
    font_s = pygame.font.SysFont(None, 24)
    init_fonts(font_l, font_m, font_s)
    manager = SceneManager(StatevectorDemo(None))
    manager.scene.manager = manager
    while True:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            manager.handle_event(event)
        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()

