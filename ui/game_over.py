import pygame
import math
from utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, MENU_BG_COLOR, BTN_BLUE,
    BTN_YELLOW, BTN_GREEN, TEXT_COLOR, TEXT_ORANGE
)


class GameOverMenu:
    def __init__(self, is_win):
        self.is_win = is_win
        self.font_title = pygame.font.SysFont(None, 40, bold=True)
        self.font_s = pygame.font.SysFont(None, 18, bold=True)

        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((40, 40, 35, 180))

        pw, ph = 340, 360
        self.rect_body = pygame.Rect(WINDOW_WIDTH // 2 - pw // 2, WINDOW_HEIGHT // 2 - ph // 2, pw, ph)

        cx = self.rect_body.centerx
        cy = self.rect_body.bottom - 70
        btn_r = 35

        if self.is_win:
            self.buttons = [
                {'pos': (cx - 100, cy), 'r': btn_r, 'color': BTN_YELLOW, 'name': 'Replay'},
                {'pos': (cx, cy),       'r': btn_r, 'color': BTN_BLUE,   'name': 'Levels'},
                {'pos': (cx + 100, cy), 'r': btn_r, 'color': BTN_GREEN,  'name': 'Next'},
            ]
        else:
            self.buttons = [
                {'pos': (cx - 60, cy), 'r': btn_r, 'color': BTN_YELLOW, 'name': 'Replay'},
                {'pos': (cx + 60, cy), 'r': btn_r, 'color': BTN_BLUE,   'name': 'Levels'},
            ]

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))

        pygame.draw.rect(screen, MENU_BG_COLOR, self.rect_body, border_radius=20)
        border_color = (200, 200, 200) if self.is_win else TEXT_ORANGE
        pygame.draw.rect(screen, border_color, self.rect_body, width=3, border_radius=20)

        msg = "YOU WIN!" if self.is_win else "THIEF ESCAPED!"
        tcolor = TEXT_COLOR if self.is_win else TEXT_ORANGE
        title = self.font_title.render(msg, True, tcolor)
        screen.blit(title, (self.rect_body.centerx - title.get_width() // 2, self.rect_body.y + 40))

        gc = self.rect_body.centerx
        gy = self.rect_body.y + 140
        if self.is_win:
            for i, offset in enumerate([-60, 0, 60]):
                y_pos = gy - 10 if i == 1 else gy
                pygame.draw.circle(screen, BTN_YELLOW, (gc + offset, y_pos), 25)
        else:
            pygame.draw.rect(screen, (100, 100, 100), (gc - 40, gy - 40, 80, 80), border_radius=10)
            ttxt = self.font_s.render("[ THIEF ]", True, (255, 255, 255))
            screen.blit(ttxt, (gc - ttxt.get_width() // 2, gy - ttxt.get_height() // 2))

        for b in self.buttons:
            pos = b['pos']
            r = b['r']
            pygame.draw.circle(screen, b['color'], pos, r)
            pygame.draw.circle(screen, (0, 0, 0), pos, r, width=2)

            if b['name'] == 'Replay':
                pygame.draw.circle(screen, (0, 0, 0), pos, 15, width=3)
                pygame.draw.polygon(screen, (0, 0, 0), [(pos[0], pos[1] - 15), (pos[0] - 10, pos[1] - 10), (pos[0], pos[1] - 5)])
                pygame.draw.polygon(screen, (0, 0, 0), [(pos[0] - 5, pos[1] - 5), (pos[0] - 5, pos[1] + 5), (pos[0] + 5, pos[1])])
            elif b['name'] == 'Levels':
                gap = 6
                for dy in [-gap, 0, gap]:
                    pygame.draw.line(screen, (0, 0, 0), (pos[0] - 12, pos[1] + dy), (pos[0] + 12, pos[1] + dy), 3)
            elif b['name'] == 'Next':
                pygame.draw.polygon(screen, (0, 0, 0), [(pos[0] - 10, pos[1] - 10), (pos[0] - 10, pos[1] + 10), (pos[0], pos[1])])
                pygame.draw.polygon(screen, (0, 0, 0), [(pos[0], pos[1] - 10), (pos[0], pos[1] + 10), (pos[0] + 10, pos[1])])

            ltxt = self.font_s.render(b['name'], True, (100, 100, 100))
            screen.blit(ltxt, (pos[0] - ltxt.get_width() // 2, pos[1] + r + 5))

    def handle_click(self, pos):
        def dist(p1, p2): return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
        for b in self.buttons:
            if dist(pos, b['pos']) <= b['r']:
                return b['name'].upper()
        return None
