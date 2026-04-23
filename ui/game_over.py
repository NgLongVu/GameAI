import pygame
import math
import os
import utils.constants as const

ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons')

def load_icon(name, size):
    path = os.path.join(ICON_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, (size, size))


class GameOverMenu:
    def __init__(self, is_win):
        self.is_win = is_win
        self.font_title = pygame.font.SysFont(None, 40, bold=True)
        self.font_s = pygame.font.SysFont(None, 18, bold=True)

        self.overlay = pygame.Surface((const.WINDOW_WIDTH, const.WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((40, 40, 35, 180))

        pw, ph = 340, 360
        self.rect_body = pygame.Rect(const.WINDOW_WIDTH // 2 - pw // 2, const.WINDOW_HEIGHT // 2 - ph // 2, pw, ph)

        cx = self.rect_body.centerx
        cy = self.rect_body.bottom - 70
        btn_r = 35

        # Load Icons
        icon_size = 30
        self.icon_replay = load_icon('replay.png', icon_size)
        self.icon_levels = load_icon('menu.png', icon_size)
        self.icon_next = load_icon('1371.png', icon_size)
        # Decorative icons for result screen
        self.icon_custody = load_icon('custody.png', 80)
        self.icon_thief_escape = load_icon('2267675.png', 80)

        if self.is_win:
            self.buttons = [
                {'pos': (cx - 100, cy), 'r': btn_r, 'color': const.BTN_YELLOW, 'name': 'Replay', 'icon': self.icon_replay},
                {'pos': (cx, cy),       'r': btn_r, 'color': const.BTN_BLUE,   'name': 'Levels', 'icon': self.icon_levels},
                {'pos': (cx + 100, cy), 'r': btn_r, 'color': const.BTN_GREEN,  'name': 'Next',   'icon': self.icon_next},
            ]
        else:
            self.buttons = [
                {'pos': (cx - 60, cy), 'r': btn_r, 'color': const.BTN_YELLOW, 'name': 'Replay', 'icon': self.icon_replay},
                {'pos': (cx + 60, cy), 'r': btn_r, 'color': const.BTN_BLUE,   'name': 'Levels', 'icon': self.icon_levels},
            ]

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))

        pygame.draw.rect(screen, const.MENU_BG_COLOR, self.rect_body, border_radius=20)
        border_color = (200, 200, 200) if self.is_win else const.TEXT_ORANGE
        pygame.draw.rect(screen, border_color, self.rect_body, width=3, border_radius=20)

        msg = "YOU WIN!" if self.is_win else "THIEF ESCAPED!"
        tcolor = const.TEXT_COLOR if self.is_win else const.TEXT_ORANGE
        title = self.font_title.render(msg, True, tcolor)
        screen.blit(title, (self.rect_body.centerx - title.get_width() // 2, self.rect_body.y + 40))

        gc = self.rect_body.centerx
        gy = self.rect_body.y + 140
        if self.is_win:
            # Show custody icon (police arresting thief)
            custody_rect = self.icon_custody.get_rect(center=(gc, gy))
            screen.blit(self.icon_custody, custody_rect)
        else:
            # Show thief escaping icon
            escape_rect = self.icon_thief_escape.get_rect(center=(gc, gy))
            screen.blit(self.icon_thief_escape, escape_rect)

        for b in self.buttons:
            pos = b['pos']
            r = b['r']
            # Drop shadow
            pygame.draw.circle(screen, (40, 40, 40), (pos[0], pos[1] + 4), r)
            # Main button
            pygame.draw.circle(screen, b['color'], pos, r)
            pygame.draw.circle(screen, (0, 0, 0), pos, r, width=3)

            # Draw icon inside button
            icon = b['icon']
            icon_rect = icon.get_rect(center=pos)
            screen.blit(icon, icon_rect)

            ltxt = self.font_s.render(b['name'], True, (100, 100, 100))
            screen.blit(ltxt, (pos[0] - ltxt.get_width() // 2, pos[1] + r + 5))

    def handle_click(self, pos):
        def dist(p1, p2): return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
        for b in self.buttons:
            if dist(pos, b['pos']) <= b['r']:
                return b['name'].upper()
        return None
