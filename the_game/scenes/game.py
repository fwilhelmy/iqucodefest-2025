import pygame, sys, itertools
import networkx as nx
from settings import WHITE, BLACK, GREEN
from core.scene import Scene

# colour palette for node types
TYPE_COLOUR = {
    1: ( 50, 140, 255),   # blue
    2: (255, 70,  70 ),   # red
    3: (255, 200,  40),   # yellow
    4: (255, 210,   0),   # gold
}

class GameScene(Scene):
    """
    Renders a directed graph.  Players can walk along outgoing edges
    with ← / → (cycle) and ↵ (confirm) for demo purposes.
    """
    def __init__(self, manager, players, n_turns, map_module):
        super().__init__(manager)
        self.players, self.n_turns = players, n_turns

        # ── build graph ────────────────────────────────────────────────
        self.g: nx.DiGraph = map_module.build_graph()

        # We keep an “active” node per player; just use player 0 for now
        self.active_idx = 0
        self.active_node = list(self.g.nodes)[0]      # start on first node
        self.edge_iter = itertools.cycle(self.g.successors(self.active_node))

        self.font = pygame.font.SysFont(None, 28)
        self.big  = pygame.font.SysFont(None, 42)

    # ── simple navigation demo ─────────────────────────────────────────
    def _pick_next_edge(self):
        """Rotate cursor to the next outgoing edge."""
        for _ in range(len(self.g)):
            nxt = next(self.edge_iter)
            if self.g.has_edge(self.active_node, nxt):
                return nxt
        return self.active_node

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:          # back to menu
                from scenes.menu import MenuScene
                self.manager.go_to(MenuScene(self.manager))
            elif e.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.cursor_target = self._pick_next_edge()
            elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                # move the pawn
                if hasattr(self, "cursor_target"):
                    self.active_node = self.cursor_target
                    self.edge_iter = itertools.cycle(self.g.successors(self.active_node))
                    # Award a star if the node is of type 4
                    if self.g.nodes[self.active_node].get("type") == 4:
                        self.players[self.active_idx].add_stars(1)

        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    def update(self, dt): pass    # no physics yet

    # ── drawing helpers ────────────────────────────────────────────────
    def _draw_edges(self, s):
        for u, v in self.g.edges:
            x1, y1 = self.g.nodes[u]["pos"]
            x2, y2 = self.g.nodes[v]["pos"]
            pygame.draw.line(s, BLACK, (x1, y1), (x2, y2), 3)
            # little arrow-head
            vx, vy = x2 - x1, y2 - y1
            length = max((vx*vx + vy*vy) ** 0.5, 1)
            ux, uy = vx / length, vy / length
            perp = (-uy, ux)
            tip  = (x2 - ux * 20, y2 - uy * 20)
            left = (tip[0] + perp[0]*8, tip[1] + perp[1]*8)
            rght = (tip[0] - perp[0]*8, tip[1] - perp[1]*8)
            pygame.draw.polygon(s, BLACK, [ (x2,y2), left, rght ])

    def _draw_nodes(self, s):
        for n, data in self.g.nodes(data=True):
            x, y = data["pos"]
            col  = TYPE_COLOUR[data["type"]]
            pygame.draw.circle(s, col, (x,y), 30)
            pygame.draw.circle(s, BLACK, (x,y), 30, 3)

            if data["type"] in (1,2):
                label = str(data["value"])
            elif data["type"] == 3:
                label = "⊕"
            else:  # type 4
                label = "★"

            img = self.big.render(label, True, BLACK)
            s.blit(img, img.get_rect(center=(x,y)))

        # active pawn
        ax, ay = self.g.nodes[self.active_node]["pos"]
        pygame.draw.circle(s, (0,0,0), (ax,ay), 12)

        # highlight cursor target, if any
        if hasattr(self, "cursor_target"):
            tx, ty = self.g.nodes[self.cursor_target]["pos"]
            pygame.draw.circle(s, GREEN, (tx,ty), 36, 4)

    def draw(self, s):
        s.fill(WHITE)
        self._draw_edges(s)
        self._draw_nodes(s)

        # HUD
        txt = self.font.render(
            f"Node {self.active_node}   |   {self.n_turns} turns total",
            True, BLACK)
        s.blit(txt, (10, 10))

        # Display star count for each player
        for i, p in enumerate(self.players):
            info = self.font.render(f"{p.name}: {p.stars}★", True, BLACK)
            s.blit(info, (10, 40 + i*20))
