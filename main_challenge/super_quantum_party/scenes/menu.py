import pygame, sys
from super_quantum_party.settings import BLACK, WHITE, GREEN, MAP_FILES, MAP_THUMBS, WIDTH, HEIGHT
from super_quantum_party.models.player import Player
from super_quantum_party.ui import widgets                   
from super_quantum_party.core.scene import Scene
from super_quantum_party.scenes.game import GameScene  
   
from importlib import import_module


TextInput   = widgets.TextInput          
DropDown    = widgets.DropDown
ToggleGroup = widgets.ToggleGroup
ImageSelect = widgets.ImageSelect
Button      = widgets.Button
class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        # background image
        self.background = pygame.image.load("super_quantum_party/resources/superquantumparty.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # ── background music ────────────────────────────────────────────
        pygame.mixer.music.load("super_quantum_party/resources/audio/menu_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%

        # ─── build UI ────────────────────────────────────────────────
        self.players_ui=[]

        self.turn_toggle = ToggleGroup((300,420), [10,15,20,25])
        self.map_select  = ImageSelect(MAP_THUMBS, (264, 450))
        self.play_btn    = Button("Play!", (900,500))

        order_opts=[1,2,3,4]
        # Keep all drop downs vertically aligned
        for id in range(4):
            idx = 3-id
            y=180+idx*45
            name = TextInput((150,y,180,28), f"Player {idx+1}")
            prio = DropDown((455, y, 60, 28), order_opts, idx+1)
            self.players_ui.append((name, prio))

        self.all_players = [Player(i) for i in range(4)]

    # ─── helper ──────────────────────────────────────────────────────
    def _collect_menu_data(self):
        for p,(name_ui,dd) in zip(self.all_players, self.players_ui):
            p.set_name(name_ui.text or f"Player{p.slot+1}")
            p.set_turn_priority(dd.value)
        return self.all_players, self.turn_toggle.value

    # ─── Scene overrides ────────────────────────────────────────────
    def handle_event(self, e):
        for n,d in self.players_ui: n.handle_event(e); d.handle_event(e)
        self.turn_toggle.handle_event(e); self.map_select.handle_event(e)

        if self.play_btn.handle_event(e):
            pygame.mixer.music.stop()
            players, n_turns = self._collect_menu_data()
            idx         = self.map_select.index        # 0,1,2…
            module_path = MAP_FILES[idx]               # maps.example_map
            map_module  = import_module(module_path)   # real Python module
            self.manager.go_to(
                GameScene(self.manager, players, n_turns, map_module)
            )


        if e.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit(); sys.exit()

    def update(self, dt): pass

    def draw(self, s):
        # draw background centered without scaling
        bg_rect = self.background.get_rect(center=s.get_rect().center)
        s.blit(self.background, bg_rect)

        # translucent panel for menu elements
        # panel = pygame.Surface((980, 420), pygame.SRCALPHA)
        # panel.fill((255, 255, 255, 220))
        # s.blit(panel, (60, 120))
        # pygame.draw.rect(s, BLACK, pygame.Rect(60, 120, 980, 420), 2)

        title = widgets.FONT_L.render("Super Quantum Party", True, (255,255,0))
        s.blit(title, title.get_rect(center=(s.get_width()//2, 50)))

        for i in range(4):
            y=180+i*45
            s.blit(widgets.FONT_S.render(f"Player {i+1} :",True,BLACK),(65,y+4))
            s.blit(widgets.FONT_S.render("Turn Priority:",True,BLACK),(350,y+4))

        for n,d in self.players_ui: n.draw(s); d.draw(s)
        s.blit(widgets.FONT_M.render("Number of turns :",True,BLACK),(65,400))
        self.turn_toggle.draw(s)
        s.blit(widgets.FONT_M.render("Map selection :",True,BLACK),(65,450))
        self.map_select.draw(s)
        self.play_btn.draw(s)
