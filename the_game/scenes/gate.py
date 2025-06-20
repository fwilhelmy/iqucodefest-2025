import pygame
import sys
from .gateGame.CircuitSimulator import CircuitSimulator
from .gateGame.GameUI import GameUI
from qiskit import QuantumCircuit
from qiskit_aer.noise import NoiseModel, depolarizing_error

from settings import WIDTH, HEIGHT, WHITE, BLACK, GREEN
from core.scene import Scene
from ui.widgets import Button

class GateScene(Scene):
    GATE_COLORS = {"H": (200,200,255),"Z": (255,200,200),"Y": (200,255,200),"X": (255,255,200),"CNOT": (200,255,255),"SWAP": (255,200,255), "DECOH": (120,120,120)}
    GATE_LIST = ["H","Z","Y","X","CNOT","SWAP"]
    MAX_GATES = 20

    def __init__(self, manager, players, n_turns, map_module, previous_scene=None):
        super().__init__(manager)
        self.players = players
        self.n_turns = n_turns
        self.map_module = map_module
        # reference to the GameScene to return to
        self.previous_scene = previous_scene
        # Always ensure all gates are present for each player
        for p in self.players:
            if not hasattr(p, "gates") or not isinstance(p.gates, dict):
                p.gates = {gate: 2 for gate in self.GATE_LIST}
            else:
                # Add missing gates with value 0
                for gate in self.GATE_LIST:
                    if gate not in p.gates:
                        p.gates[gate] = 0
        self.current_player = 0
        self.skipped_players = set()
        self.gate_rects = {}
        for i, gate in enumerate(self.GATE_LIST):
            self.gate_rects[gate] = pygame.Rect(30, 50 + i*60, 80, 40)
        self.qiskit_circuit = CircuitSimulator.create_empty_circuit()
        self.gate_history = [("H", 0), ("H", 1, "layer0")]
        self.dragging_gate = None
        self.drag_offset = (0,0)
        self.drag_pos = (0,0)
        self.measurement_result = None
        self.font = pygame.font.SysFont(None, 32)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.continue_button = Button("Continue", (self.WIDTH - 180, 30))

    def get_decoherence_percent(self):
        decoh_gates = [g for g in self.gate_history if g[0] == "DECOH"]
        percent = min(100, len(decoh_gates) * 20)
        return percent

    def next_player(self):
        n = len(self.players)
        for _ in range(n):
            self.current_player = (self.current_player + 1) % n
            if self.current_player not in self.skipped_players:
                return

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # Compute button rects without drawing
            skip_btn_rect = pygame.Rect(self.WIDTH - 350, self.HEIGHT - 80, 120, 50)
            btn_rect = pygame.Rect(self.WIDTH - 180, self.HEIGHT - 80, 150, 50)
            if skip_btn_rect.collidepoint(mx, my):
                self.skipped_players.add(self.current_player)
                self.next_player()
                self.dragging_gate = None
                self.drag_pos = (0,0)
                return
            for gate, rect in self.gate_rects.items():
                if rect.collidepoint(mx, my) and self.players[self.current_player].gates[gate] > 0:
                    self.dragging_gate = gate
                    self.drag_offset = (mx - rect.x, my - rect.y)
                    self.drag_pos = (mx, my)
            if btn_rect.collidepoint(mx, my):
                percent = self.get_decoherence_percent()
                noise_model = CircuitSimulator.apply_decoherence_noise(self.qiskit_circuit, percent)
                self.measurement_result = CircuitSimulator.apply_circuit(self.qiskit_circuit, noise_model=noise_model, gate_history=self.gate_history)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_gate:
                mx, my = event.pos
                base_x = 200
                gate_layer = max(0, len(self.gate_history) - 2)
                drop_x = base_x + (gate_layer+2)*60
                dropped = False
                for q in range(2):
                    y = 150 + q*60
                    if drop_x-20 < mx < drop_x+20 and y-20 < my < y+20:
                        if self.dragging_gate == "CNOT":
                            control = q
                            target = 1 - q
                            self.qiskit_circuit.cx(control, target)
                            self.gate_history.append(("CNOT", control, target))
                            self.players[self.current_player].gates["CNOT"] -= 1
                            self.next_player()
                            self.measurement_result = None
                            dropped = True
                            break
                        elif self.dragging_gate == "SWAP":
                            self.qiskit_circuit.swap(0, 1)
                            self.gate_history.append(("SWAP", 0, 1))
                            self.players[self.current_player].gates["SWAP"] -= 1
                            self.next_player()
                            self.measurement_result = None
                            dropped = True
                            break
                        else:
                            if self.dragging_gate == "H":
                                self.qiskit_circuit.h(q)
                            elif self.dragging_gate == "X":
                                self.qiskit_circuit.x(q)
                            elif self.dragging_gate == "Y":
                                self.qiskit_circuit.y(q)
                            elif self.dragging_gate == "Z":
                                self.qiskit_circuit.z(q)
                            self.gate_history.append((self.dragging_gate, q))
                            self.players[self.current_player].gates[self.dragging_gate] -= 1
                            self.next_player()
                            self.measurement_result = None
                            dropped = True
                            break
                placed_gates = [g for g in self.gate_history[2:] if g[0] != "DECOH"]
                if len(placed_gates) > 0 and len(placed_gates) % 4 == 0:
                    self.gate_history.append(("DECOH", None))
                self.dragging_gate = None
                self.drag_pos = (0,0)
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_gate:
                self.drag_pos = event.pos
        if self.continue_button.handle_event(event):
            if self.previous_scene is not None:
                self.previous_scene.apply_measurement(self.measurement_result or "00")
                self.manager.go_to(self.previous_scene)
            else:
                from scenes.game import GameScene
                self.manager.go_to(
                    GameScene(self.manager, self.players, self.n_turns, self.map_module)
                )

    def update(self, dt):
        pass  # No time-based updates needed for this minigame

    def draw(self, screen):
        screen.fill((240,240,240))
        GameUI.draw_player_info(screen, self.font, self.players, self.current_player)
        GameUI.draw_gates(screen, self.font, self.players[self.current_player], self.players, self.current_player, self.gate_rects, self.GATE_LIST, self.GATE_COLORS)
        GameUI.draw_circuit(screen, self.font, self.gate_history, self.GATE_COLORS, self.MAX_GATES)
        btn_rect = GameUI.draw_measure_button(screen, self.font, self.WIDTH, self.HEIGHT)
        skip_btn_rect = GameUI.draw_skip_button(screen, self.font, self.WIDTH, self.HEIGHT)
        decoh_percent = self.get_decoherence_percent()
        decoh_txt = self.font.render(f"Decoherence chance: {decoh_percent}%", True, (120,0,0))
        screen.blit(decoh_txt, (self.WIDTH-350, self.HEIGHT-180))
        if self.measurement_result:
            txt = self.font.render(f"Measured: {self.measurement_result}", True, (0,0,0))
            screen.blit(txt, (self.WIDTH-300, self.HEIGHT-140))
        if self.dragging_gate:
            mx, my = self.drag_pos
            pygame.draw.rect(screen, self.GATE_COLORS[self.dragging_gate], (mx-40, my-20, 80, 40))
            txt = self.font.render(self.dragging_gate, True, (0,0,0))
            screen.blit(txt, (mx-20, my-10))
        self.continue_button.draw(screen)