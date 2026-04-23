import pygame
import math
import utils.constants as const
from utils.audio_manager import AudioManager


class SettingsMenu:
    def __init__(self):
        self.font_title = pygame.font.SysFont(None, 32, bold=True)
        self.font_normal = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 22)

        self.overlay = pygame.Surface((const.WINDOW_WIDTH, const.WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((40, 40, 35, 180))

        pw, ph = 420, 300
        self.rect_body = pygame.Rect(const.WINDOW_WIDTH // 2 - pw // 2, const.WINDOW_HEIGHT // 2 - ph // 2, pw, ph)
        self.rect_header = pygame.Rect(self.rect_body.x, self.rect_body.y, pw, 60)
        self.btn_close = {'pos': (self.rect_header.right - 25, self.rect_header.centery), 'r': 20}

        # Slider dimensions — wider track, more padding
        slider_w = 200
        slider_h = 14
        lx = self.rect_body.x + 40
        rx = self.rect_body.x + 130
        start_y = self.rect_body.y + 120
        gap = 80

        self.sfx_slider = pygame.Rect(rx, start_y - slider_h // 2, slider_w, slider_h)
        self.music_slider = pygame.Rect(rx, start_y + gap - slider_h // 2, slider_w, slider_h)

        self.knob_radius = 14
        self.dragging = None  # 'sfx' or 'music' or None

        self.audio = AudioManager()

    def _get_knob_x(self, slider_rect, volume):
        return int(slider_rect.x + volume * slider_rect.width)

    def _volume_from_x(self, slider_rect, x):
        vol = (x - slider_rect.x) / slider_rect.width
        return max(0.0, min(1.0, vol))

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))

        # Body
        pygame.draw.rect(screen, const.POPUP_BODY, self.rect_body, border_radius=15)
        pygame.draw.rect(screen, (80, 80, 80), self.rect_body, width=3, border_radius=15)

        # Header
        pygame.draw.rect(screen, const.POPUP_HEADER, self.rect_header,
                         border_top_left_radius=15, border_top_right_radius=15)
        pygame.draw.rect(screen, (50, 50, 50), self.rect_header, width=3,
                         border_top_left_radius=15, border_top_right_radius=15)

        title = self.font_title.render("SETTINGS", True, const.TEXT_COLOR)
        screen.blit(title, (self.rect_header.centerx - title.get_width() // 2,
                             self.rect_header.centery - title.get_height() // 2))

        # Close Button
        pygame.draw.circle(screen, (255, 255, 255), self.btn_close['pos'], self.btn_close['r'])
        pygame.draw.circle(screen, (50, 50, 50), self.btn_close['pos'], self.btn_close['r'], width=3)
        cx, cy = self.btn_close['pos']
        pygame.draw.line(screen, (50, 50, 50), (cx - 7, cy - 7), (cx + 7, cy + 7), 3)
        pygame.draw.line(screen, (50, 50, 50), (cx + 7, cy - 7), (cx - 7, cy + 7), 3)

        # Labels
        lx = self.rect_body.x + 40
        start_y = self.rect_body.y + 120
        gap = 80

        screen.blit(self.font_normal.render("SFX", True, const.TEXT_COLOR), (lx, start_y - 12))
        screen.blit(self.font_normal.render("Music", True, const.TEXT_COLOR), (lx, start_y + gap - 12))

        # Sliders
        self._draw_slider(screen, self.sfx_slider, self.audio.sfx_volume)
        self._draw_slider(screen, self.music_slider, self.audio.music_volume)

        # Volume percentage
        sfx_pct = f"{int(self.audio.sfx_volume * 100)}%"
        music_pct = f"{int(self.audio.music_volume * 100)}%"
        sfx_txt = self.font_small.render(sfx_pct, True, (80, 80, 80))
        music_txt = self.font_small.render(music_pct, True, (80, 80, 80))
        screen.blit(sfx_txt, (self.sfx_slider.right + 14, self.sfx_slider.centery - sfx_txt.get_height() // 2))
        screen.blit(music_txt, (self.music_slider.right + 14, self.music_slider.centery - music_txt.get_height() // 2))

    def _draw_slider(self, screen, slider_rect, volume):
        # Track background (rounded)
        pygame.draw.rect(screen, const.TOGGLE_OFF, slider_rect, border_radius=7)
        # Filled portion
        fill_w = max(1, int(slider_rect.width * volume))
        filled = pygame.Rect(slider_rect.x, slider_rect.y, fill_w, slider_rect.height)
        pygame.draw.rect(screen, const.TOGGLE_ON, filled, border_radius=7)
        # Track border
        pygame.draw.rect(screen, (80, 80, 80), slider_rect, width=2, border_radius=7)
        # Knob
        knob_x = self._get_knob_x(slider_rect, volume)
        knob_y = slider_rect.centery
        # Knob shadow
        pygame.draw.circle(screen, (180, 180, 180), (knob_x + 1, knob_y + 1), self.knob_radius)
        # Knob fill
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, knob_y), self.knob_radius)
        # Knob border
        pygame.draw.circle(screen, (50, 50, 50), (knob_x, knob_y), self.knob_radius, width=3)

    def handle_click(self, pos):
        def dist(p1, p2): return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

        if dist(pos, self.btn_close['pos']) <= self.btn_close['r']:
            return "CLOSE_SETTINGS"

        # Check if clicking on a slider knob or track
        sfx_knob = (self._get_knob_x(self.sfx_slider, self.audio.sfx_volume), self.sfx_slider.centery)
        music_knob = (self._get_knob_x(self.music_slider, self.audio.music_volume), self.music_slider.centery)

        expanded_sfx = self.sfx_slider.inflate(0, 40)
        expanded_music = self.music_slider.inflate(0, 40)

        if dist(pos, sfx_knob) <= self.knob_radius + 8 or expanded_sfx.collidepoint(pos):
            self.dragging = 'sfx'
            vol = self._volume_from_x(self.sfx_slider, pos[0])
            self.audio.set_sfx_volume(vol)
            self.audio.play_sfx('click')
        elif dist(pos, music_knob) <= self.knob_radius + 8 or expanded_music.collidepoint(pos):
            self.dragging = 'music'
            vol = self._volume_from_x(self.music_slider, pos[0])
            self.audio.set_music_volume(vol)

        return None

    def handle_drag(self, pos):
        """Call this on MOUSEMOTION when dragging a slider."""
        if self.dragging == 'sfx':
            vol = self._volume_from_x(self.sfx_slider, pos[0])
            self.audio.set_sfx_volume(vol)
        elif self.dragging == 'music':
            vol = self._volume_from_x(self.music_slider, pos[0])
            self.audio.set_music_volume(vol)

    def handle_release(self):
        """Call this on MOUSEBUTTONUP to stop dragging."""
        self.dragging = None
