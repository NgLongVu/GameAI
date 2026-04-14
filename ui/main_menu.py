import pygame
import math
from utils.constants import (
    WINDOW_WIDTH, MENU_BG_COLOR, BTN_BLUE, BTN_DARK,
    TEXT_COLOR, TEXT_LIGHT
)


class MainMenu:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 48, bold=True)
        self.font_normal = pygame.font.SysFont(None, 24)

        self.btn_settings = {'pos': (80, 80), 'r': 40}
        self.btn_burger = {'pos': (500, 700), 'r': 40}
        self.btn_play = {'pos': (300, 550), 'r': 80}
        self.coins_rect = pygame.Rect(400, 50, 120, 50)
        self.graphic_rect = pygame.Rect(150, 250, 300, 150)

    def draw(self, screen):
        screen.fill(MENU_BG_COLOR)

        # Settings (Top Left)
        pygame.draw.circle(screen, BTN_BLUE, self.btn_settings['pos'], self.btn_settings['r'])
        pygame.draw.circle(screen, (0, 0, 0), self.btn_settings['pos'], self.btn_settings['r'] // 2, width=4)

        # Coins Box (Top Right)
        pygame.draw.rect(screen, BTN_DARK, self.coins_rect, border_radius=10)
        ctext = self.font_normal.render("50", True, TEXT_LIGHT)
        screen.blit(ctext, (self.coins_rect.centerx - ctext.get_width() // 2 + 10,
                             self.coins_rect.centery - ctext.get_height() // 2))
        pygame.draw.circle(screen, (255, 215, 0), (self.coins_rect.x + 30, self.coins_rect.centery), 10)

        # Title
        title = self.font_title.render("CATCH THE THIEF", True, TEXT_COLOR)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 170))

        # Center Graphic Mockup
        pygame.draw.rect(screen, (200, 200, 200), self.graphic_rect, border_radius=10)
        pygame.draw.rect(screen, BTN_DARK, self.graphic_rect, width=3, border_radius=10)
        ptext = self.font_normal.render("[ ART GRAPHIC MOCKUP ]", True, TEXT_COLOR)
        screen.blit(ptext, (self.graphic_rect.centerx - ptext.get_width() // 2,
                             self.graphic_rect.centery - ptext.get_height() // 2))

        # Play Button (Center)
        pygame.draw.circle(screen, BTN_BLUE, self.btn_play['pos'], self.btn_play['r'])
        x, y = self.btn_play['pos']
        r = 30
        pygame.draw.polygon(screen, (0, 0, 0), [
            (x - r // 2, y - r), (x - r // 2, y + r), (x + r, y)
        ])

        # Hamburger Menu (Bottom Right)
        pygame.draw.circle(screen, BTN_BLUE, self.btn_burger['pos'], self.btn_burger['r'])
        hx, hy = self.btn_burger['pos']
        hwidth = 20
        pygame.draw.line(screen, (0, 0, 0), (hx - hwidth, hy - 10), (hx + hwidth, hy - 10), 4)
        pygame.draw.line(screen, (0, 0, 0), (hx - hwidth, hy), (hx + hwidth, hy), 4)
        pygame.draw.line(screen, (0, 0, 0), (hx - hwidth, hy + 10), (hx + hwidth, hy + 10), 4)

    def handle_click(self, pos):
        def dist(p1, p2): return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

        if dist(pos, self.btn_play['pos']) <= self.btn_play['r']:
            return "PLAY_LEVEL_1"
        if dist(pos, self.btn_settings['pos']) <= self.btn_settings['r']:
            return "OPEN_SETTINGS"
        if dist(pos, self.btn_burger['pos']) <= self.btn_burger['r']:
            return "OPEN_LEVEL_SELECT"
        return None
