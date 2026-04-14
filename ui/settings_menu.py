import pygame
import math
from utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TEXT_COLOR,
    POPUP_HEADER, POPUP_BODY, TOGGLE_ON, TOGGLE_OFF
)


class SettingsMenu:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 30, bold=True)
        self.font_normal = pygame.font.SysFont(None, 24)

        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((40, 40, 35, 180))

        pw, ph = 320, 340
        self.rect_body = pygame.Rect(WINDOW_WIDTH // 2 - pw // 2, WINDOW_HEIGHT // 2 - ph // 2, pw, ph)
        self.rect_header = pygame.Rect(self.rect_body.x, self.rect_body.y, pw, 60)
        self.btn_close = {'pos': (self.rect_header.right - 20, self.rect_header.centery), 'r': 18}

        lx = self.rect_body.x + 40
        rx = self.rect_body.right - 90
        start_y = self.rect_body.y + 110
        gap = 60

        self.sound_rect = pygame.Rect(rx, start_y - 12, 60, 30)
        self.music_rect = pygame.Rect(rx, start_y + gap - 12, 60, 30)
        self.lang_rect = pygame.Rect(rx, start_y + 2 * gap - 12, 60, 30)

        self.sound_state = True
        self.music_state = True
        self.lang_state = "EN"

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))

        # Body
        pygame.draw.rect(screen, POPUP_BODY, self.rect_body, border_radius=15)
        pygame.draw.rect(screen, (150, 150, 150), self.rect_body, width=2, border_radius=15)

        # Header
        pygame.draw.rect(screen, POPUP_HEADER, self.rect_header,
                         border_top_left_radius=15, border_top_right_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), self.rect_header, width=2,
                         border_top_left_radius=15, border_top_right_radius=15)

        title = self.font_title.render("SETTINGS", True, TEXT_COLOR)
        screen.blit(title, (self.rect_header.centerx - title.get_width() // 2,
                             self.rect_header.centery - title.get_height() // 2))

        # Close Button
        pygame.draw.circle(screen, (255, 255, 255), self.btn_close['pos'], self.btn_close['r'])
        pygame.draw.circle(screen, (0, 0, 0), self.btn_close['pos'], self.btn_close['r'], width=2)
        cx, cy = self.btn_close['pos']
        pygame.draw.line(screen, (0, 0, 0), (cx - 6, cy - 6), (cx + 6, cy + 6), 2)
        pygame.draw.line(screen, (0, 0, 0), (cx + 6, cy - 6), (cx - 6, cy + 6), 2)

        # Labels
        lx = self.rect_body.x + 40
        start_y = self.rect_body.y + 110
        gap = 60
        screen.blit(self.font_normal.render("Sound", True, TEXT_COLOR), (lx, start_y - 8))
        screen.blit(self.font_normal.render("Music", True, TEXT_COLOR), (lx, start_y + gap - 8))
        screen.blit(self.font_normal.render("Language", True, TEXT_COLOR), (lx, start_y + 2 * gap - 8))

        # Toggles
        def draw_toggle(rect, state):
            color = TOGGLE_ON if state else TOGGLE_OFF
            pygame.draw.rect(screen, color, rect, border_radius=15)
            pygame.draw.rect(screen, (0, 0, 0), rect, width=2, border_radius=15)
            circ_x = rect.right - 15 if state else rect.left + 15
            pygame.draw.circle(screen, (255, 255, 255), (circ_x, rect.centery), 11)
            pygame.draw.circle(screen, (0, 0, 0), (circ_x, rect.centery), 11, width=1)

        draw_toggle(self.sound_rect, self.sound_state)
        draw_toggle(self.music_rect, self.music_state)

        # Language button
        pygame.draw.rect(screen, (255, 255, 255), self.lang_rect, border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), self.lang_rect, width=1, border_radius=5)
        ltxt = self.font_normal.render(self.lang_state, True, TEXT_COLOR)
        screen.blit(ltxt, (self.lang_rect.centerx - ltxt.get_width() // 2,
                            self.lang_rect.centery - ltxt.get_height() // 2))

    def handle_click(self, pos):
        def dist(p1, p2): return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

        if dist(pos, self.btn_close['pos']) <= self.btn_close['r']:
            return "CLOSE_SETTINGS"

        if self.sound_rect.collidepoint(pos):
            self.sound_state = not self.sound_state
        elif self.music_rect.collidepoint(pos):
            self.music_state = not self.music_state
        elif self.lang_rect.collidepoint(pos):
            self.lang_state = "VN" if self.lang_state == "EN" else "EN"

        return None
