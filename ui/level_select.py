import pygame
import math
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BTN_BLUE, BTN_LOCKED


class LevelSelectMenu:
    def __init__(self):
        self.font_num = pygame.font.SysFont(None, 36, bold=True)

        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((40, 40, 35, 220))

        self.btn_back = {'pos': (80, 80), 'r': 40}

        self.level_buttons = []
        start_y = 400
        start_x = 120
        gap = 120
        for i in range(8):
            row = i // 4
            col = i % 4
            cx = start_x + col * gap
            cy = start_y + row * gap
            self.level_buttons.append({'level': i + 1, 'pos': (cx, cy), 'r': 45})

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))

        # Back Button
        pygame.draw.circle(screen, BTN_BLUE, self.btn_back['pos'], self.btn_back['r'])
        bx, by = self.btn_back['pos']
        pygame.draw.polygon(screen, (0, 0, 0), [
            (bx + 10, by - 15), (bx + 10, by + 15), (bx - 15, by)
        ])

        # Level Buttons
        for btn in self.level_buttons:
            lvl = btn['level']
            pos = btn['pos']
            r = btn['r']

            if lvl <= 4:
                pygame.draw.circle(screen, BTN_BLUE, pos, r)
                pygame.draw.circle(screen, (0, 0, 0), pos, r, 2)
                txt = self.font_num.render(str(lvl), True, (0, 0, 0))
            else:
                pygame.draw.circle(screen, BTN_LOCKED, pos, r)
                pygame.draw.circle(screen, (0, 0, 0), pos, r, 2)
                txt = self.font_num.render(str(lvl), True, (0, 0, 0))
                lock_rect = pygame.Rect(pos[0] - 8, pos[1] + 10, 16, 12)
                pygame.draw.rect(screen, (255, 180, 0), lock_rect, border_radius=2)
                pygame.draw.circle(screen, (255, 180, 0), (pos[0], pos[1] + 10), 6, width=2)

            screen.blit(txt, (pos[0] - txt.get_width() // 2,
                               pos[1] - txt.get_height() // 2 - (5 if lvl > 4 else 0)))

    def handle_click(self, pos):
        def dist(p1, p2): return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

        if dist(pos, self.btn_back['pos']) <= self.btn_back['r']:
            return "BACK_TO_MENU"

        for btn in self.level_buttons:
            if dist(pos, btn['pos']) <= btn['r']:
                if btn['level'] <= 4:
                    return f"PLAY_LEVEL_{btn['level']}"
                return None  # Locked

        return None
