import pygame
import math
import os
import utils.constants as const
from utils.save_manager import SaveManager

ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons')
IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images')

def load_icon(name, size):
    path = os.path.join(ICON_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, (size, size))


class MainMenu:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 56, bold=True)
        self.font_normal = pygame.font.SysFont(None, 24)
        self.save_manager = SaveManager()

        self.btn_settings = {'pos': (80, 80), 'r': 40}
        self.btn_burger = {'pos': (const.WINDOW_WIDTH - 80, const.WINDOW_HEIGHT - 80), 'r': 40}
        self.btn_play = {'pos': (const.WINDOW_WIDTH // 2, const.WINDOW_HEIGHT - 200), 'r': 70}
        self.coins_rect = pygame.Rect(const.WINDOW_WIDTH - 150, 50, 120, 50)

        # Load full-screen background
        self.bg_full = None
        bg_path = os.path.join(IMAGES_DIR, 'bgmenu.png')
        if os.path.exists(bg_path):
            raw = pygame.image.load(bg_path).convert()
            self.bg_full = pygame.transform.smoothscale(raw, (const.WINDOW_WIDTH, const.WINDOW_HEIGHT))

        # Load Icons
        self.icon_settings = load_icon('settings.png', 50)
        self.icon_play = load_icon('play-button-arrowhead.png', 60)
        self.icon_burger = load_icon('menu (1).png', 50)

    def draw(self, screen):
        # Full-screen background
        if self.bg_full:
            screen.blit(self.bg_full, (0, 0))
        else:
            screen.fill(const.MENU_BG_COLOR)

        # Settings (Top Left)
        pygame.draw.circle(screen, (40, 40, 40), (self.btn_settings['pos'][0], self.btn_settings['pos'][1] + 4), self.btn_settings['r'])
        pygame.draw.circle(screen, const.BTN_BLUE, self.btn_settings['pos'], self.btn_settings['r'])
        pygame.draw.circle(screen, (0, 0, 0), self.btn_settings['pos'], self.btn_settings['r'], width=3)
        icon_rect = self.icon_settings.get_rect(center=self.btn_settings['pos'])
        screen.blit(self.icon_settings, icon_rect)

        # Coins Box (Top Right)
        pygame.draw.rect(screen, const.BTN_DARK, self.coins_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.coins_rect, width=2, border_radius=10)
        ctext = self.font_normal.render(str(self.save_manager.get_coins()), True, const.TEXT_LIGHT)
        screen.blit(ctext, (self.coins_rect.centerx - ctext.get_width() // 2 + 10,
                             self.coins_rect.centery - ctext.get_height() // 2))
        pygame.draw.circle(screen, (255, 215, 0), (self.coins_rect.x + 30, self.coins_rect.centery), 10)

        # Title with shadow
        title = self.font_title.render("CATCH THE THIEF", True, const.TEXT_COLOR)
        shadow = self.font_title.render("CATCH THE THIEF", True, (200, 200, 200))
        screen.blit(shadow, (const.WINDOW_WIDTH // 2 - title.get_width() // 2 + 2, 172))
        screen.blit(title, (const.WINDOW_WIDTH // 2 - title.get_width() // 2, 170))

        # Play Button (Center) with icon
        pygame.draw.circle(screen, (40, 40, 40), (self.btn_play['pos'][0], self.btn_play['pos'][1] + 6), self.btn_play['r'])
        pygame.draw.circle(screen, const.BTN_BLUE, self.btn_play['pos'], self.btn_play['r'])
        pygame.draw.circle(screen, (0, 0, 0), self.btn_play['pos'], self.btn_play['r'], width=4)
        play_rect = self.icon_play.get_rect(center=self.btn_play['pos'])
        screen.blit(self.icon_play, play_rect)

        # Hamburger Menu (Bottom Right) with icon
        pygame.draw.circle(screen, (40, 40, 40), (self.btn_burger['pos'][0], self.btn_burger['pos'][1] + 4), self.btn_burger['r'])
        pygame.draw.circle(screen, const.BTN_BLUE, self.btn_burger['pos'], self.btn_burger['r'])
        pygame.draw.circle(screen, (0, 0, 0), self.btn_burger['pos'], self.btn_burger['r'], width=3)
        burger_rect = self.icon_burger.get_rect(center=self.btn_burger['pos'])
        screen.blit(self.icon_burger, burger_rect)

    def handle_click(self, pos):
        def dist(p1, p2): return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

        if dist(pos, self.btn_play['pos']) <= self.btn_play['r']:
            return "PLAY_LATEST"
        if dist(pos, self.btn_settings['pos']) <= self.btn_settings['r']:
            return "OPEN_SETTINGS"
        if dist(pos, self.btn_burger['pos']) <= self.btn_burger['r']:
            return "OPEN_LEVEL_SELECT"
        return None
