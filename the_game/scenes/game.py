import pygame, sys, random
import networkx as nx
from settings import WIDTH, HEIGHT, WHITE, BLACK, GREEN
from core.scene import Scene
from ui.widgets import Button

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
    with left/right arrows (cycle) and Enter (confirm) for demo purposes.
    """
    CAM_SPEED = 400  # pixels per second
    MOVE_SPEED = 200  # speed for walking animation (px/s)

    def __init__(self, manager, players, n_turns, map_module):
        super().__init__(manager)
        self.players = sorted(players, key=lambda p: p.order)
        self.n_turns = n_turns  # remaining turns

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
        self.pending_rolls = []          # store dice rolled so far

        self.font = pygame.font.SysFont(None, 28)
        self.big  = pygame.font.SysFont(None, 42)

        # button used to roll the dice one at a time
        self.roll_button = Button("Roll", (WIDTH - 80, HEIGHT - 40))

        # Camera offset when drawing large maps
        self.cam_x = 0
        self.cam_y = 0
        self.zoom  = 1.0

        # movement animation state
        self.steps_remaining = 0
        self.moving_player = None
        self.move_target = None
        self.move_progress = 0.0
        self.player_anim_pos = {
            p: list(self.g.nodes[self.start_node]["pos"]) for p in self.players
        }
        self.branch_choices = None

    # ── simple navigation demo ─────────────────────────────────────────
    def _start_move(self, target):
        """Begin animating towards ``target`` for the active player."""
        self.move_target = target
        self.move_progress = 0.0
        self.moving_player = self.players[self.active_idx]

    def _begin_walk(self, player, steps):
        """Queue a walking animation of ``steps`` nodes for ``player``."""
        self.steps_remaining = steps
        self.moving_player = player
        self.player_anim_pos[player] = list(self.g.nodes[player.position]["pos"])

    def _roll_one_die(self):
        """Roll a single die and store the result."""
        value = random.randint(1, 6)
        self.pending_rolls.append(value)

        # When both dice are rolled, move the player
        if len(self.pending_rolls) == 2:
            player = self.players[self.active_idx]
            d1, d2 = self.pending_rolls
            steps = d1 + d2
            self.last_roll = (
                player.name or f"P{player.slot+1}", d1, d2, steps
            )
            self.pending_rolls.clear()
            self._begin_walk(player, steps)

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:          # back to menu
                from scenes.menu import MenuScene
                self.manager.go_to(MenuScene(self.manager))

            elif e.key in (pygame.K_SPACE, pygame.K_RETURN):
                if not self.steps_remaining:
                    self._roll_one_die()

            elif e.key in (pygame.K_KP_PLUS, pygame.K_EQUALS):
                self.zoom = min(self.zoom * 1.25, 4)
            elif e.key in (pygame.K_KP_MINUS, pygame.K_MINUS):
                self.zoom = max(self.zoom / 1.25, 0.25)

            elif self.branch_choices:
                if pygame.K_1 <= e.key <= pygame.K_9:
                    idx = e.key - pygame.K_1
                    if idx < len(self.branch_choices):
                        self._start_move(self.branch_choices[idx])
                        self.branch_choices = None

        if self.roll_button.handle_event(e):
            if not self.steps_remaining:
                self._roll_one_die()

        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    def update(self, dt):
        keys = pygame.key.get_pressed()
        spd = self.CAM_SPEED * dt
        if keys[pygame.K_LEFT]:  self.cam_x += spd
        if keys[pygame.K_RIGHT]: self.cam_x -= spd
        if keys[pygame.K_UP]:    self.cam_y += spd
        if keys[pygame.K_DOWN]:  self.cam_y -= spd

        # handle walking animation
        if self.move_target:
            p = self.moving_player
            x1, y1 = self.player_anim_pos[p]
            tx, ty = self.g.nodes[self.move_target]["pos"]
            dx, dy = tx - x1, ty - y1
            dist = (dx*dx + dy*dy) ** 0.5
            if dist:
                step = self.MOVE_SPEED * dt
                if step >= dist:
                    self.player_anim_pos[p] = [tx, ty]
                    p.position = self.move_target
                    self.move_target = None
                    self.move_progress = 0.0
                    self.steps_remaining -= 1
                    # award star on landing
                    if self.g.nodes[p.position].get("type") == 4:
                        p.add_stars(1)
                else:
                    ux, uy = dx/dist, dy/dist
                    self.player_anim_pos[p][0] += ux * step
                    self.player_anim_pos[p][1] += uy * step

        elif self.steps_remaining > 0 and not self.branch_choices:
            p = self.moving_player
            current = p.position
            succ = list(self.g.successors(current))
            if not succ:
                self.steps_remaining = 0
            elif len(succ) == 1:
                self._start_move(succ[0])
            else:
                self.branch_choices = succ
        elif self.steps_remaining == 0 and self.moving_player:
            self.active_idx = (self.active_idx + 1) % len(self.players)
            self.n_turns -= 1
            self.moving_player = None
            if self.n_turns <= 0:
                from scenes.winner import WinnerScene
                self.manager.go_to(WinnerScene(self.manager, self.players))

    # ── drawing helpers ────────────────────────────────────────────────
    def _draw_edges(self, s):
        for u, v in self.g.edges:
            x1, y1 = self.g.nodes[u]["pos"]
            x2, y2 = self.g.nodes[v]["pos"]
            x1 = (x1 + self.cam_x) * self.zoom
            y1 = (y1 + self.cam_y) * self.zoom
            x2 = (x2 + self.cam_x) * self.zoom
            y2 = (y2 + self.cam_y) * self.zoom
            pygame.draw.line(s, BLACK, (x1, y1), (x2, y2), max(1,int(3*self.zoom)))
            # little arrow-head
            vx, vy = x2 - x1, y2 - y1
            length = max((vx*vx + vy*vy) ** 0.5, 1)
            ux, uy = vx / length, vy / length
            perp = (-uy, ux)
            size = 20 * self.zoom
            tip  = (x2 - ux * size, y2 - uy * size)
            left = (tip[0] + perp[0]*8*self.zoom, tip[1] + perp[1]*8*self.zoom)
            rght = (tip[0] - perp[0]*8*self.zoom, tip[1] - perp[1]*8*self.zoom)
            pygame.draw.polygon(s, BLACK, [ (x2,y2), left, rght ])

    def _draw_nodes(self, s):
        radius = int(20 * self.zoom)
        for n, data in self.g.nodes(data=True):
            x, y = data["pos"]
            x = (x + self.cam_x) * self.zoom
            y = (y + self.cam_y) * self.zoom
            col  = TYPE_COLOUR[data["type"]]
            pygame.draw.circle(s, col, (x,y), radius)
            pygame.draw.circle(s, BLACK, (x,y), radius, 2)

            if data["type"] in (1,2):
                label = str(data.get("value", ""))
            elif data["type"] == 3:
                label = "X"  # previously used ⊕ which may not render
            else:  # type 4
                label = "*"  # previously used ★ which may not render

            img = self.big.render(label, True, BLACK)
            s.blit(img, img.get_rect(center=(x,y)))

        # highlight branch options
        if self.branch_choices:
            for i,node in enumerate(self.branch_choices):
                x,y = self.g.nodes[node]["pos"]
                x = (x + self.cam_x) * self.zoom
                y = (y + self.cam_y) * self.zoom
                txt = self.font.render(str(i+1), True, BLACK)
                r = txt.get_rect(center=(x, y - radius - 10))
                s.blit(txt, r)

        # draw players on top of nodes
        self._draw_players(s)

    def _draw_players(self, s):
        offsets = [(-15,-40), (15,-40), (-15,-60), (15,-60)]
        for idx, p in enumerate(self.players):
            x, y = self.player_anim_pos.get(p, self.g.nodes[p.position]["pos"])
            x = (x + self.cam_x) * self.zoom
            y = (y + self.cam_y) * self.zoom
            dx, dy = offsets[idx % len(offsets)]
            dx *= self.zoom; dy *= self.zoom
            if p.sprite:
                sprite = pygame.transform.smoothscale(
                    p.sprite, (int(p.sprite.get_width()*self.zoom), int(p.sprite.get_height()*self.zoom))
                ) if self.zoom != 1 else p.sprite
                r = sprite.get_rect(center=(x+dx, y+dy))
                s.blit(sprite, r)
            else:
                pygame.draw.circle(s, p.color, (x+dx, y+dy), int(12*self.zoom))
            if idx == self.active_idx:
                pygame.draw.circle(s, GREEN, (x+dx, y+dy), int(14*self.zoom), 2)

    def draw(self, s):
        s.fill(WHITE)
        self._draw_edges(s)
        self._draw_nodes(s)

        # HUD showing whose turn and last roll
        turn_name = self.players[self.active_idx].name or f"P{self.players[self.active_idx].slot+1}"
        hud = f"Turn: {turn_name}"
        if self.last_roll:
            name,d1,d2,total = self.last_roll
            hud += f"  |  {name} rolled {d1}+{d2}->{total}"  # replaced Unicode arrow
        txt = self.font.render(hud, True, BLACK)
        s.blit(txt, (10, 10))
        turns_txt = self.font.render(f"Turns left: {self.n_turns}", True, BLACK)
        s.blit(turns_txt, (WIDTH - turns_txt.get_width() - 10, 10))

        # Display stars and gate counts for each player
        for i, p in enumerate(self.players):
            gates = ", ".join(f"{g}:{c}" for g,c in p.gates.items())
            text = f"{p.name}: {p.stars}* | {gates}"  # replaced Unicode star
            info = self.font.render(text, True, BLACK)
            s.blit(info, (10, 40 + i*20))

        # Roll button
        self.roll_button.draw(s)
