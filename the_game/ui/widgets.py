"""
Menu UI controls.
Call ui.widgets.init_fonts(...) once *after* pygame.init() so the widgets
know which fonts to use.
"""
import pygame
from settings import BLACK, GREY, GREEN

# will be set by init_fonts()
FONT_L = FONT_M = FONT_S = None

def init_fonts(font_large, font_medium, font_small):
    global FONT_L, FONT_M, FONT_S
    FONT_L, FONT_M, FONT_S = font_large, font_medium, font_small

# ───────────── basic widgets ───────────────────────────────────────────
class TextInput:
    def __init__(self, rect, placeholder=""):
        self.rect = pygame.Rect(rect)
        self.text, self.placeholder = "", placeholder
        self.active = False
    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(e.pos)
        if self.active and e.type == pygame.KEYDOWN:
            if   e.key == pygame.K_RETURN:     self.active = False
            elif e.key == pygame.K_BACKSPACE:  self.text = self.text[:-1]
            else:                              self.text += e.unicode
    def draw(self, s):
        pygame.draw.rect(s, BLACK, self.rect, 2)
        txt = self.text if self.text else self.placeholder
        clr = BLACK if self.text else GREY
        s.blit(FONT_S.render(txt, True, clr), (self.rect.x+4, self.rect.y+4))

class DropDown:
    def __init__(self, rect, options, start_value):
        self.rect = pygame.Rect(rect)
        self.opts, self.value = options, start_value
        self.open = False
    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(e.pos):
                self.open = not self.open
            elif self.open:
                self.open = False
            if self.open:
                for i,opt in enumerate(self.opts):
                    r = pygame.Rect(self.rect.x, self.rect.bottom+i*self.rect.h,
                                    self.rect.w, self.rect.h)
                    if r.collidepoint(e.pos):
                        self.value, self.open = opt, False
    def draw(self,s):
        pygame.draw.rect(s, BLACK, self.rect, 2)
        s.blit(FONT_S.render(str(self.value), True, BLACK),
               (self.rect.x+4, self.rect.y+4))
        pygame.draw.polygon(s, BLACK,
            [(self.rect.right-14,self.rect.y+10),
             (self.rect.right-4 ,self.rect.y+10),
             (self.rect.right-9 ,self.rect.y+18)])
        if self.open:
            for i,opt in enumerate(self.opts):
                r = pygame.Rect(self.rect.x, self.rect.bottom+i*self.rect.h,
                                self.rect.w, self.rect.h)
                pygame.draw.rect(s,(200,200,200),r)
                pygame.draw.rect(s,BLACK,r,1)
                s.blit(FONT_S.render(str(opt),True,BLACK),(r.x+4,r.y+4))

class ToggleGroup:
    def __init__(self, center, values):
        self.values, self.index = values, 0
        self.buttons=[]
        x,y=center
        for i,v in enumerate(values):
            r=pygame.Rect(0,0,70,36); r.center=(x+i*80,y)
            self.buttons.append(r)
    @property
    def value(self): return self.values[self.index]
    def handle_event(self,e):
        if e.type==pygame.MOUSEBUTTONDOWN:
            for i,r in enumerate(self.buttons):
                if r.collidepoint(e.pos): self.index=i
    def draw(self,s):
        for i,r in enumerate(self.buttons):
            pygame.draw.rect(s,BLACK,r,2)
            if i==self.index: pygame.draw.rect(s,(180,230,180),r.inflate(-4,-4))
            s.blit(FONT_S.render(str(self.values[i]),True,BLACK),
                   FONT_S.render("0",True,BLACK).get_rect(center=r.center))

class ImageSelect:
    def __init__(self, images, pos):
        self.thumb_rects, self.images = [], []
        x,y=pos
        for idx,fn in enumerate(images):
            img=pygame.transform.smoothscale(pygame.image.load(fn),(150,150))
            r  = img.get_rect(topleft=(x+idx*220, y))
            self.images.append(img); self.thumb_rects.append(r)
        self.index=0; self.files=images
    @property
    def filename(self): return self.files[self.index]
    def handle_event(self,e):
        if e.type==pygame.MOUSEBUTTONDOWN:
            for i,r in enumerate(self.thumb_rects):
                if r.collidepoint(e.pos): self.index=i
    def draw(self,s):
        for i,r in enumerate(self.thumb_rects):
            s.blit(self.images[i],r)
            pygame.draw.rect(s, GREEN if i==self.index else BLACK, r,4)

class Button:
    def __init__(self, text, center):
        self.image = FONT_L.render(text, True, BLACK)
        self.rect  = self.image.get_rect(center=center)
    def handle_event(self,e): return e.type==pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos)
    def draw(self,s): 
        s.blit(self.image,self.rect)
        pygame.draw.rect(s,BLACK,self.rect,3)
