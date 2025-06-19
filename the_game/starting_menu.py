import pygame
import sys

pygame.init()
pygame.display.set_caption("Super Quantum Party")
WIDTH, HEIGHT = 1100, 650
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK  = pygame.time.Clock()
FONT_L = pygame.font.SysFont(None, 72)
FONT_M = pygame.font.SysFont(None, 32)
FONT_S = pygame.font.SysFont(None, 24)

# -------------------------------------------------------------------------
# Domain model – your real Player class will replace this one later
# -------------------------------------------------------------------------
class Player:
    def __init__(self, slot):
        self.slot = slot
        self.name = ""
        self.order = slot + 1   # default 1–4
    # -- placeholder setters you’ll replace with real game logic ----------
    def set_name(self, name):   self.name  = name
    def set_turn_priority(self, order): self.order = order
    # --------------------------------------------------------------------

# -------------------------------------------------------------------------
# UI widgets
# -------------------------------------------------------------------------
class TextInput:
    def __init__(self, rect, placeholder=""):
        self.rect = pygame.Rect(rect)
        self.text = ""
        self.placeholder = placeholder
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, surf):
        pygame.draw.rect(surf, (0,0,0), self.rect, 2)
        txt = self.text if self.text else self.placeholder
        color = (0,0,0) if self.text else (120,120,120)
        img = FONT_S.render(txt, True, color)
        surf.blit(img, (self.rect.x+4, self.rect.y+4))

class DropDown:
    def __init__(self, rect, options, start_value):
        self.rect  = pygame.Rect(rect)
        self.opts  = options
        self.value = start_value
        self.open  = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
            elif self.open:
                # clicked outside – close menu
                self.open = False
            # pick option?
            if self.open:
                for i,opt in enumerate(self.opts):
                    r = pygame.Rect(self.rect.x, self.rect.bottom+i*self.rect.h,
                                    self.rect.w, self.rect.h)
                    if r.collidepoint(event.pos):
                        self.value = opt
                        self.open  = False

    def draw(self, surf):
        pygame.draw.rect(surf, (0,0,0), self.rect, 2)
        img = FONT_S.render(str(self.value), True, (0,0,0))
        surf.blit(img, (self.rect.x+4, self.rect.y+4))
        # arrow
        pygame.draw.polygon(surf,(0,0,0),
            [(self.rect.right-14,self.rect.y+10),
             (self.rect.right-4 ,self.rect.y+10),
             (self.rect.right-9 ,self.rect.y+18)])
        # options
        if self.open:
            for i,opt in enumerate(self.opts):
                r = pygame.Rect(self.rect.x, self.rect.bottom+i*self.rect.h,
                                self.rect.w, self.rect.h)
                pygame.draw.rect(surf,(200,200,200),r)
                pygame.draw.rect(surf,(0,0,0),r,1)
                img = FONT_S.render(str(opt), True, (0,0,0))
                surf.blit(img,(r.x+4,r.y+4))

class ToggleGroup:
    """Simple horizontal toggle buttons (for # of turns)."""
    def __init__(self, center, values):
        self.values = values
        self.index  = 0
        self.buttons = []
        x,y = center
        for i,v in enumerate(values):
            rect = pygame.Rect(0,0,70,36)
            rect.center = (x + i*80, y)
            self.buttons.append(rect)

    @property
    def value(self):
        return self.values[self.index]

    def handle_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            for i,rect in enumerate(self.buttons):
                if rect.collidepoint(event.pos):
                    self.index = i

    def draw(self,surf):
        for i,rect in enumerate(self.buttons):
            sel = (i==self.index)
            pygame.draw.rect(surf,(0,0,0),rect,2)
            if sel:
                pygame.draw.rect(surf,(180,230,180),rect.inflate(-4,-4))
            txt = FONT_S.render(str(self.values[i]),True,(0,0,0))
            surf.blit(txt,txt.get_rect(center=rect.center))

class ImageSelect:
    """Draws square thumbnails, highlights the chosen one."""
    def __init__(self, images, pos):
        self.thumb_rects = []
        self.images = []
        x,y = pos
        for idx,fn in enumerate(images):
            img = pygame.image.load(fn).convert_alpha()
            img = pygame.transform.smoothscale(img,(150,150))
            r   = img.get_rect()
            r.topleft = (x+idx*220, y)
            self.thumb_rects.append(r)
            self.images.append(img)
        self.index = 0

    @property
    def filename(self):
        return ['map1.png','map2.png','map3.png'][self.index]

    def handle_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            for i,r in enumerate(self.thumb_rects):
                if r.collidepoint(event.pos):
                    self.index = i

    def draw(self,surf):
        for i,r in enumerate(self.thumb_rects):
            surf.blit(self.images[i], r)
            col = (0,220,0) if i==self.index else (0,0,0)
            pygame.draw.rect(surf,col,r,4)

class Button:
    def __init__(self, text, center):
        self.image = FONT_L.render(text, True, (0,0,0))
        self.rect  = self.image.get_rect()
        self.rect.center = center

    def handle_event(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

    def draw(self,surf):
        surf.blit(self.image,self.rect)
        pygame.draw.rect(surf,(0,0,0),self.rect,3)

# -------------------------------------------------------------------------
# Build widget instances
# -------------------------------------------------------------------------
players_ui = []
order_options = [1,2,3,4]
for idx in range(4):
    y = 150 + idx*45
    name_box = TextInput( (150, y, 180, 28), f"Player {idx+1}" )
    order_dd  = DropDown  ( (455 + (idx*60), y, 60, 28), order_options, idx+1 )
    players_ui.append((name_box, order_dd))

turn_toggle = ToggleGroup( (300, 360), [10,15,20,25] )
map_select = ImageSelect( ["../resources/map1.png","../resources/map2.png","../resources/map3.png"], (80, 450) )
play_btn    = Button("Play!", (900, 500))   # a bit lower

# -------------------------------------------------------------------------
# Main loop
# -------------------------------------------------------------------------
all_players = [Player(i) for i in range(4)]  # create now, fill later

def apply_ui_to_players():
    for i,(txt,dd) in enumerate(players_ui):
        all_players[i].set_name(txt.text or f"Player{i+1}")
        all_players[i].set_turn_priority(dd.value)
    # at this point you also have:
    #   turn_toggle.value   -> number of turns
    #   map_select.filename -> chosen map file name
    # Replace this print block with real scene-loading code -------------
    print("\n===== Start Game =====")
    print("Turns   :", turn_toggle.value)
    print("Map     :", map_select.filename)
    for p in all_players:
        print(f"{p.name:10s}  priority {p.order}")
    print("======================\n")
    # placeholder for scene switch
    pygame.time.wait(1500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   running=False
        # dispatch events
        for namebox,drop in players_ui:
            namebox.handle_event(event)
            drop.handle_event(event)
        turn_toggle.handle_event(event)
        map_select.handle_event(event)
        if play_btn.handle_event(event):
            apply_ui_to_players()

    # ---- draw --------------------------------------------------------
    SCREEN.fill((255,255,255))
    title = FONT_L.render("Super Quantum Party", True, (0,0,0))
    SCREEN.blit(title, title.get_rect(center=(WIDTH//2, 60)))

    # labels
    for i in range(4):
        y = 150+i*45
        lbl = FONT_S.render(f"Player {i+1} :", True, (0,0,0))
        SCREEN.blit(lbl,(40,y+4))
        prio = FONT_S.render("Turn Priority:",True,(0,0,0))
        SCREEN.blit(prio,(350,y+4))

    for namebox,drop in players_ui:
        namebox.draw(SCREEN); drop.draw(SCREEN)

    # number-of-turns section
    SCREEN.blit(FONT_M.render("Number of turns :",True,(0,0,0)),(50,350))
    turn_toggle.draw(SCREEN)

    # map section
    SCREEN.blit(FONT_M.render("Map selection :",True,(40,0,0)), (50,400))
    map_select.draw(SCREEN)

    play_btn.draw(SCREEN)

    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
sys.exit()
