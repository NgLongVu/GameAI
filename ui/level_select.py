import pygame
import math
import os
import utils.constants as const
from utils.save_manager import SaveManager

ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons')

def load_icon(name, size):
    path = os.path.join(ICON_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, (size, size))


class LevelSelectMenu:
    def __init__(self):
        self.font_num = pygame.font.SysFont(None, 36, bold=True)
        self.save_manager = SaveManager()

        self.overlay = pygame.Surface((const.WINDOW_WIDTH, const.WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((40, 40, 35, 220))

        self.btn_back = {'pos': (80, 80), 'r': 40}

        # Load Icons
        self.icon_back = load_icon('back.png', 50)
        self.icon_lock = load_icon('lock.png', 28)

        self.level_buttons = []
        cols = 3
        gap = min(const.WINDOW_WIDTH // 4, 120)
        # Calculate total width of the grid to center it perfectly
        grid_width = (cols - 1) * gap
        start_x = (const.WINDOW_WIDTH - grid_width) // 2
        start_y = const.WINDOW_HEIGHT // 2 - 120
        for i in range(8):
            row = i // cols
            col = i % cols
            cx = start_x + col * gap
            cy = start_y + row * gap
            self.level_buttons.append({'level': i + 1, 'pos': (cx, cy), 'r': 40})

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))

        # Back Button with icon
        pygame.draw.circle(screen, (40, 40, 40), (self.btn_back['pos'][0], self.btn_back['pos'][1] + 4), self.btn_back['r'])
        pygame.draw.circle(screen, const.BTN_BLUE, self.btn_back['pos'], self.btn_back['r'])
        pygame.draw.circle(screen, (0, 0, 0), self.btn_back['pos'], self.btn_back['r'], width=3)
        back_rect = self.icon_back.get_rect(center=self.btn_back['pos'])
        screen.blit(self.icon_back, back_rect)

        # Level Buttons
        for btn in self.level_buttons:
            lvl = btn['level']
            pos = btn['pos']
            r = btn['r']

            if lvl <= self.save_manager.get_max_level():
                pygame.draw.circle(screen, (40, 40, 40), (pos[0], pos[1] + 4), r)
                pygame.draw.circle(screen, const.BTN_BLUE, pos, r)
                pygame.draw.circle(screen, (0, 0, 0), pos, r, 3)
                txt = self.font_num.render(str(lvl), True, (0, 0, 0))
                screen.blit(txt, (pos[0] - txt.get_width() // 2,
                                   pos[1] - txt.get_height() // 2))
            else:
                pygame.draw.circle(screen, (40, 40, 40), (pos[0], pos[1] + 4), r)
                pygame.draw.circle(screen, const.BTN_LOCKED, pos, r)
                pygame.draw.circle(screen, (0, 0, 0), pos, r, 3)
                txt = self.font_num.render(str(lvl), True, (0, 0, 0))
                screen.blit(txt, (pos[0] - txt.get_width() // 2,
                                   pos[1] - txt.get_height() // 2 - 8))
                # Lock icon below the number
                lock_rect = self.icon_lock.get_rect(center=(pos[0], pos[1] + 16))
                screen.blit(self.icon_lock, lock_rect)

    def handle_click(self, pos):
        def dist(p1, p2): return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

        if dist(pos, self.btn_back['pos']) <= self.btn_back['r']:
            return "BACK_TO_MENU"

        for btn in self.level_buttons:
            if dist(pos, btn['pos']) <= btn['r']:
                if btn['level'] <= self.save_manager.get_max_level():
                    return f"PLAY_LEVEL_{btn['level']}"
                return None  # Locked

        return None
