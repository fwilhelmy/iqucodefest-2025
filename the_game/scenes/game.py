import pygame, sys, random
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
        self.players = sorted(players, key=lambda p: p.order)
        self.n_turns = n_turns

        # ── build graph ────────────────────────────────────────────────
        self.g: nx.DiGraph = map_module.build_graph()
        self.start_node = list(self.g.nodes)[0]

        # assign basic sprites/colours and starting positions
        colours = [
            (60,120,240), (230,60,60),
            (60,180,80), (190,80,200)
        ]
        for idx,p in enumerate(self.players):
            p.position = self.start_node
            col = colours[idx % len(colours)]
            p.color = col
            surf = pygame.Surface((24,24), pygame.SRCALPHA)
            pygame.draw.circle(surf, col, (12,12), 12)
            p.set_sprite(surf)

        self.active_idx = 0
        self.last_roll = None

        self.font = pygame.font.SysFont(None, 28)
        self.big  = pygame.font.SysFont(None, 42)

    # ── simple navigation demo ─────────────────────────────────────────
    def _move_player(self, player, steps):
        current = player.position
        for _ in range(steps):
            succ = list(self.g.successors(current))
            if not succ:
                break
            current = random.choice(succ)
        player.position = current

    def roll_and_move(self):
        player = self.players[self.active_idx]
        d1, d2 = random.randint(1,6), random.randint(1,6)
        steps = d1 + d2
        self.last_roll = (player.name or f"P{player.slot+1}", d1, d2, steps)
        self._move_player(player, steps)
        self.active_idx = (self.active_idx + 1) % len(self.players)

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
            elif e.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.roll_and_move()

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

        # draw players on top of nodes
        self._draw_players(s)

    def _draw_players(self, s):
        offsets = [(-15,-40), (15,-40), (-15,-60), (15,-60)]
        for idx, p in enumerate(self.players):
            x, y = self.g.nodes[p.position]["pos"]
            dx, dy = offsets[idx % len(offsets)]
            if p.sprite:
                r = p.sprite.get_rect(center=(x+dx, y+dy))
                s.blit(p.sprite, r)
            else:
                pygame.draw.circle(s, p.color, (x+dx, y+dy), 12)
            if idx == self.active_idx:
                pygame.draw.circle(s, GREEN, (x+dx, y+dy), 14, 2)

    def draw(self, s):
        s.fill(WHITE)
        self._draw_edges(s)
        self._draw_nodes(s)

        # HUD showing whose turn and last roll
        turn_name = self.players[self.active_idx].name or f"P{self.players[self.active_idx].slot+1}"
        hud = f"Turn: {turn_name}"
        if self.last_roll:
            name,d1,d2,total = self.last_roll
            hud += f"  |  {name} rolled {d1}+{d2}→{total}"
        txt = self.font.render(hud, True, BLACK)
        s.blit(txt, (10, 10))

        # Display star count for each player
        for i, p in enumerate(self.players):
            info = self.font.render(f"{p.name}: {p.stars}★", True, BLACK)
            s.blit(info, (10, 40 + i*20))
