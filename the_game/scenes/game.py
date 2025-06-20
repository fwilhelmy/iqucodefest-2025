import pygame, sys, random
import networkx as nx
from the_game.settings import WIDTH, HEIGHT, WHITE, BLACK, GREEN
from the_game.core.scene import Scene
from the_game.ui.widgets import Button

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
    MOVE_DELAY = 0.4  # seconds between steps when walking

    ZOOM_STEP = 0.1

    def _clamp_zoom(self, zoom: float) -> float:
        """Clamp zoom level to a sane range."""
        return max(0.2, min(zoom, 3.0))


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
        # load dice roll sound
        self.dice_sound = pygame.mixer.Sound("resources/audio/dice_roll.mp3")

        # Camera offset when drawing large maps
        self.cam_x = 0
        self.cam_y = 0
        self.zoom = 1.0

        # movement animation state
        self.moving_player = None
        self.steps_remaining = 0
        self.move_timer = 0
        self.awaiting_choice = False
        self.branch_options = []
        self.branch_index = 0

    # ── simple navigation demo ─────────────────────────────────────────
    def _start_move(self, player, steps):
        """Begin walking ``steps`` spaces with animation."""
        self.moving_player = player
        self.steps_remaining = steps
        self.move_timer = 0
        self.awaiting_choice = False
        self.branch_options = []
        self.branch_index = 0

    def _end_move(self):
        """Finish the current player's move and handle turn logic."""
        current = self.moving_player.position
        if self.g.nodes[current].get("type") == 4:
            self.moving_player.add_stars(1)
        self.moving_player = None
        self.steps_remaining = 0
        self.pending_rolls.clear()
        self.active_idx = (self.active_idx + 1) % len(self.players)
        if self.active_idx == 0:
            # If all players have had their turn, reduce the turn count
            self.n_turns -= 1
            if self.n_turns <= 0:
                from scenes.winner import WinnerScene
                self.manager.go_to(WinnerScene(self.manager, self.players))
            else:
                print("BATTTTTTLEEEE!!!")
                # TODO SWITCH TO QUANTUM BATTLE SCENE

    def _roll_one_die(self):
        """Roll a single die and store the result."""
        value = random.randint(1, 6)
        # play dice roll sound
        self.dice_sound.play()
        self.pending_rolls.append(value)

        # When both dice are rolled, start walking animation
        if len(self.pending_rolls) == 2 and self.moving_player is None:
            player = self.players[self.active_idx]
            d1, d2 = self.pending_rolls
            steps = d1 + d2
            self.last_roll = (
                player.name or f"P{player.slot+1}", d1, d2, steps
            )
            self._start_move(player, steps)

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            from the_game.scenes.menu import MenuScene
            self.manager.go_to(MenuScene(self.manager))
        elif self.moving_player is None:
            roll_keys = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_r)
            if self.roll_button.handle_event(e) or (e.type == pygame.KEYDOWN and e.key in roll_keys):
                self._roll_one_die()
        elif self.awaiting_choice and e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                next_node = self.branch_options[self.branch_index]
                self.moving_player.position = next_node
                self.steps_remaining -= 1
                self.awaiting_choice = False
                self.move_timer = self.MOVE_DELAY
                if self.steps_remaining <= 0:
                    self._end_move()
            elif e.key == pygame.K_MINUS:
                self.zoom = self._clamp_zoom(self.zoom - self.ZOOM_STEP)
            elif e.key == pygame.K_EQUALS:
                self.zoom = self._clamp_zoom(self.zoom + self.ZOOM_STEP)
            elif e.key == pygame.K_LEFT:
                self.branch_index = (self.branch_index - 1) % len(self.branch_options)
            elif e.key == pygame.K_RIGHT:
                self.branch_index = (self.branch_index + 1) % len(self.branch_options)
        elif e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        

    def update(self, dt):
        keys = pygame.key.get_pressed()
        spd = self.CAM_SPEED * dt / self.zoom
        if keys[pygame.K_LEFT]:  self.cam_x += spd
        if keys[pygame.K_RIGHT]: self.cam_x -= spd
        if keys[pygame.K_UP]:    self.cam_y += spd
        if keys[pygame.K_DOWN]:  self.cam_y -= spd

        if self.moving_player and not self.awaiting_choice:
            self.move_timer -= dt
            if self.move_timer <= 0:
                current = self.moving_player.position
                succ = list(self.g.successors(current))
                if not succ:
                    self._end_move()
                elif len(succ) > 1:
                    self.awaiting_choice = True
                    self.branch_options = succ
                    self.branch_index = 0
                else:
                    self.moving_player.position = succ[0]
                    self.steps_remaining -= 1
                    self.move_timer = self.MOVE_DELAY
                    if self.steps_remaining <= 0:
                        self._end_move()

    # ── drawing helpers ────────────────────────────────────────────────
    def _draw_edges(self, s):
        for u, v in self.g.edges:
            x1, y1 = self.g.nodes[u]["pos"]
            x2, y2 = self.g.nodes[v]["pos"]
            x1 = x1 * self.zoom + self.cam_x
            y1 = y1 * self.zoom + self.cam_y
            x2 = x2 * self.zoom + self.cam_x
            y2 = y2 * self.zoom + self.cam_y
            width = max(1, int(3 * self.zoom))
            pygame.draw.line(s, BLACK, (x1, y1), (x2, y2), width)
            # little arrow-head
            vx, vy = x2 - x1, y2 - y1
            length = max((vx*vx + vy*vy) ** 0.5, 1)
            ux, uy = vx / length, vy / length
            perp = (-uy, ux)
            scale = 20 * self.zoom
            tip  = (x2 - ux * scale, y2 - uy * scale)
            left = (tip[0] + perp[0]*8*self.zoom, tip[1] + perp[1]*8*self.zoom)
            rght = (tip[0] - perp[0]*8*self.zoom, tip[1] - perp[1]*8*self.zoom)
            pygame.draw.polygon(s, BLACK, [ (x2,y2), left, rght ])

    def _draw_nodes(self, s):
        for n, data in self.g.nodes(data=True):
            x, y = data["pos"]
            x = x * self.zoom + self.cam_x
            y = y * self.zoom + self.cam_y
            col  = TYPE_COLOUR[data["type"]]
            radius = max(10, int(30 * self.zoom))
            pygame.draw.circle(s, col, (x, y), radius)
            pygame.draw.circle(s, BLACK, (x, y), radius, max(1, int(3 * self.zoom)))


            if data["type"] in (1,2):
                if "value" in data and data["value"] is not None:
                    label = str(data["value"])
                else:
                    digits = "".join(ch for ch in n if ch.isdigit())
                    label = digits
            elif data["type"] == 3:
                label = "X"  # previously used ⊕ which may not render
            else:  # type 4
                label = "*"  # previously used ★ which may not render

            img = self.big.render(label, True, BLACK)
            if self.zoom != 1.0:
                w = max(1, int(img.get_width() * self.zoom))
                h = max(1, int(img.get_height() * self.zoom))
                img = pygame.transform.smoothscale(img, (w, h))
            s.blit(img, img.get_rect(center=(x, y)))

        # draw players on top of nodes
        self._draw_players(s)

    def _draw_players(self, s):
        offsets = [(-15,-40), (15,-40), (-15,-60), (15,-60)]
        for idx, p in enumerate(self.players):
            x, y = self.g.nodes[p.position]["pos"]
            x = x * self.zoom + self.cam_x
            y = y * self.zoom + self.cam_y
            dx, dy = offsets[idx % len(offsets)]
            dx *= self.zoom; dy *= self.zoom
            if p.sprite:
                img = p.sprite
                if self.zoom != 1.0:
                    size = int(img.get_width() * self.zoom), int(img.get_height() * self.zoom)
                    img = pygame.transform.smoothscale(img, size)
                r = img.get_rect(center=(x+dx, y+dy))
                s.blit(img, r)
            else:
                pygame.draw.circle(s, p.color, (int(x+dx), int(y+dy)), int(12*self.zoom))
            if idx == self.active_idx:
                pygame.draw.circle(s, GREEN, (int(x+dx), int(y+dy)), int(14*self.zoom), max(1, int(2*self.zoom)))

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

        zoom_txt = self.font.render(f"Zoom: {self.zoom:.1f}x", True, BLACK)
        s.blit(zoom_txt, (WIDTH - zoom_txt.get_width() - 10, 30))

        # Display stars and gate counts for each player
        for i, p in enumerate(self.players):
            gates = ", ".join(f"{g}:{c}" for g,c in p.gates.items())
            text = f"{p.name}: {p.stars}* | {gates}"  # replaced Unicode star
            info = self.font.render(text, True, BLACK)
            s.blit(info, (10, 40 + i*20))

        # Roll button only when not walking
        if self.moving_player is None:
            self.roll_button.draw(s)

        if self.awaiting_choice:
            opts = [
                ("["+n+"]" if i==self.branch_index else n)
                for i,n in enumerate(self.branch_options)
            ]
            msg = "Choose path: " + " ".join(opts) + "  (\u2190/\u2192+Enter)"
            img = self.font.render(msg, True, BLACK)
            s.blit(img, (10, HEIGHT - 30))
