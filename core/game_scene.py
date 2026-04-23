import pygame
import math
import os

import utils.constants as const
from core.board import Board
from core.entities import Police, Thief
from core.game_state import GameState, Turn
from ui.game_over import GameOverMenu
from utils.audio_manager import AudioManager
from utils.save_manager import SaveManager

ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons')

def load_icon(name, size):
    path = os.path.join(ICON_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, (size, size))

def get_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

class GameScene:
    def __init__(self, map_path, level_name="Level 1"):
        self.level_name = level_name
        self.audio = AudioManager()
        self.save_manager = SaveManager()
        self.font = pygame.font.SysFont(None, 24)
        self.font_s = pygame.font.SysFont(None, 18)
        self.title_font = pygame.font.SysFont(None, 40)
        
        self.board = Board(map_path)
        self.police_list = [Police(n) for n in self.board.start_police]
        self.thief = Thief(self.board.start_thief)
        
        self.game_state = GameState(self.board, self.police_list, self.thief)
        self.game_state.turn_start_state_freeze = self.game_state._capture_freeze_state()
        
        # UI Rects - Reverted to center
        self.undo_rect = pygame.Rect(const.WINDOW_WIDTH // 2 - 170, const.WINDOW_HEIGHT - 100, 150, 50)
        self.freeze_rect = pygame.Rect(const.WINDOW_WIDTH // 2 + 20, const.WINDOW_HEIGHT - 100, 150, 50)
        
        # UI Setup for Top Bar
        btn_size = 50
        self.btn_settings = {'pos': (55, 55), 'r': 25}
        self.btn_replay = {'pos': (115, 55), 'r': 25}
        self.btn_home = {'pos': (55, 115), 'r': 25}
        self.coins_rect = pygame.Rect(const.WINDOW_WIDTH - 140, 30, 120, 50)
        
        # Load Icons
        icon_btn_size = 36
        self.icon_settings = load_icon('settings.png', icon_btn_size)
        self.icon_replay = load_icon('replay.png', icon_btn_size)
        self.icon_home = load_icon('home.png', icon_btn_size)
        self.icon_undo = load_icon('replay (1).png', 30)
        self.icon_freeze = load_icon('freezing.png', 30)
        self.icon_frozen_status = load_icon('freeze.png', 120)
        self.icon_frozen_status.set_alpha(180) # Make it semi-transparent
        self.audio = AudioManager()
        self.game_over_menu = None

    def handle_events(self, events):
        if self.game_over_menu:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    action = self.game_over_menu.handle_click(pygame.mouse.get_pos())
                    if action in ["REPLAY", "LEVELS", "NEXT"]:
                        return action
            return None
            
        selectable_nodes = []
        if self.game_state.turn == Turn.POLICE and not self.game_state.is_animating():
            if self.game_state.selected_police:
                selectable_nodes = self.game_state.selected_police.current_node.neighbors
                
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check Home Button
                if get_distance(mouse_pos, self.btn_home['pos']) <= self.btn_home['r']:
                    return "BACK_TO_MENU"
                if get_distance(mouse_pos, self.btn_settings['pos']) <= self.btn_settings['r']:
                    return "OPEN_SETTINGS"
                if get_distance(mouse_pos, self.btn_replay['pos']) <= self.btn_replay['r']:
                    return "REPLAY"
                
                if not self.game_state.is_animating() and self.game_state.turn == Turn.POLICE:
                    if self.undo_rect.collidepoint(mouse_pos) and self.game_state.can_undo():
                        if self.save_manager.spend_coins(10):
                            self.audio.play_sfx('undo')
                            self.game_state.undo()
                            self.game_state.history = []
                            self.game_state.turn_start_state_freeze = self.game_state._capture_freeze_state()
                        else:
                            self.audio.play_sfx('click') # Not enough coins sound
                        continue
                        
                    if self.freeze_rect.collidepoint(mouse_pos) and not self.game_state.is_thief_frozen:
                        if self.save_manager.spend_coins(15):
                            self.audio.play_sfx('freeze')
                            self.game_state.use_freeze()
                        else:
                            self.audio.play_sfx('click')
                        continue
                        
                if self.game_state.turn == Turn.POLICE and not self.game_state.is_animating():
                    moved = False
                    if self.game_state.selected_police:
                        for neighbor in self.game_state.selected_police.current_node.neighbors:
                            if get_distance((neighbor.x, neighbor.y), mouse_pos) < const.NODE_RADIUS * 1.5:
                                occupied = any(p.current_node == neighbor for p in self.police_list) or (neighbor == self.thief.current_node)
                                if not occupied:
                                    self.audio.play_sfx('move')
                                    self.game_state.process_police_move(neighbor)
                                    moved = True
                                break
                    if moved: continue
                    
                    selected = False
                    for p in self.police_list:
                        if get_distance((p.current_node.x, p.current_node.y), mouse_pos) < p.radius * 1.5:
                            self.audio.play_sfx('select')
                            self.game_state.selected_police = p
                            selected = True
                            break
                            
                    if not selected:
                        self.game_state.selected_police = None
                        
        return None

    def update(self):
        self.game_state.update()
        if not self.game_over_menu:
            if self.game_state.turn == Turn.GAME_OVER_POLICE_WIN:
                self.audio.play_sfx('win')
                self.game_over_menu = GameOverMenu(is_win=True)
                return "POLICE_WIN"
            elif self.game_state.turn == Turn.GAME_OVER_THIEF_WIN:
                self.audio.play_sfx('lose')
                self.game_over_menu = GameOverMenu(is_win=False)
                return "THIEF_WIN"
        return None

    def _draw_icon_button(self, screen, icon, pos, r, bg_color):
        """Draw a circular button with an icon centered inside and a drop shadow."""
        # Shadow
        pygame.draw.circle(screen, (40, 40, 40), (pos[0], pos[1] + 4), r)
        # Main button
        pygame.draw.circle(screen, bg_color, pos, r)
        pygame.draw.circle(screen, (0, 0, 0), pos, r, width=3)
        icon_rect = icon.get_rect(center=pos)
        screen.blit(icon, icon_rect)

    def draw(self, screen):
        # Clear screen with background color to cover any old graphics (like menu)
        screen.fill(const.BG_COLOR)
        
        selectable_nodes = []
        if self.game_state.turn == Turn.POLICE and not self.game_state.is_animating():
            if self.game_state.selected_police:
                selectable_nodes = self.game_state.selected_police.current_node.neighbors
                
        self.board.draw(screen, selectable_nodes=selectable_nodes)
        
        for p in self.police_list:
            p.draw(screen)
            
        self.thief.draw(screen)
        
        # Draw Freeze Overlay on Thief if frozen
        if self.game_state.is_thief_frozen:
            frozen_rect = self.icon_frozen_status.get_rect(center=(int(self.thief.visual_x), int(self.thief.visual_y)))
            screen.blit(self.icon_frozen_status, frozen_rect)

        # Draw Top Bar Elements with Icons
        # 1. Settings Button
        self._draw_icon_button(screen, self.icon_settings, self.btn_settings['pos'], self.btn_settings['r'], const.BTN_BLUE)
        
        # 2. Replay Button
        self._draw_icon_button(screen, self.icon_replay, self.btn_replay['pos'], self.btn_replay['r'], const.BTN_YELLOW)
        
        # 3. Home Button
        self._draw_icon_button(screen, self.icon_home, self.btn_home['pos'], self.btn_home['r'], const.BTN_BLUE)
        
        # 4. Level Text
        title_font = pygame.font.SysFont(None, 36, bold=True)
        level_txt = title_font.render(self.level_name.upper(), True, const.TEXT_COLOR)
        screen.blit(level_txt, (const.WINDOW_WIDTH//2 - level_txt.get_width()//2, 50))
        
        # 5. Coins Box
        pygame.draw.rect(screen, const.BTN_DARK, self.coins_rect, border_radius=25)
        pygame.draw.circle(screen, (255, 215, 0), (self.coins_rect.x + 30, self.coins_rect.centery), 10)
        ctext = self.font.render(str(self.save_manager.get_coins()), True, const.TEXT_LIGHT)
        screen.blit(ctext, (self.coins_rect.centerx - ctext.get_width()//2 + 10, self.coins_rect.centery - ctext.get_height()//2))
        
        # Turn/Status Text - Removed

        if self.game_state.turn in [Turn.POLICE, Turn.THIEF]:
            # Undo Button with icon
            undo_color = (150, 150, 150) if not self.game_state.can_undo() else (200, 200, 250)
            pygame.draw.rect(screen, undo_color, self.undo_rect, border_radius=10)
            pygame.draw.rect(screen, (50, 50, 50), self.undo_rect, width=3, border_radius=10)
            undo_icon_rect = self.icon_undo.get_rect(midleft=(self.undo_rect.x + 15, self.undo_rect.centery))
            screen.blit(self.icon_undo, undo_icon_rect)
            utxt = self.font.render("UNDO", True, (0,0,0))
            screen.blit(utxt, (undo_icon_rect.right + 10, self.undo_rect.centery - utxt.get_height()//2))
            # Cost Label
            cost_undo = self.font_s.render("-10 Coins", True, (100, 50, 50))
            screen.blit(cost_undo, (self.undo_rect.centerx - cost_undo.get_width()//2, self.undo_rect.bottom + 2))

            # Freeze Button with icon
            is_freeze_active = not self.game_state.is_thief_frozen
            freeze_color = (100, 255, 255) if is_freeze_active else (150, 150, 150)
            pygame.draw.rect(screen, freeze_color, self.freeze_rect, border_radius=10)
            pygame.draw.rect(screen, (50, 50, 50), self.freeze_rect, width=3, border_radius=10)
            freeze_icon_rect = self.icon_freeze.get_rect(midleft=(self.freeze_rect.x + 10, self.freeze_rect.centery))
            screen.blit(self.icon_freeze, freeze_icon_rect)
            ftxt = self.font.render("FREEZE", True, (0,0,0))
            screen.blit(ftxt, (freeze_icon_rect.right + 8, self.freeze_rect.centery - ftxt.get_height()//2))
            # Cost Label
            cost_freeze = self.font_s.render("-15 coins", True, (100, 50, 50))
            screen.blit(cost_freeze, (self.freeze_rect.centerx - cost_freeze.get_width()//2, self.freeze_rect.bottom + 2))
            
        if self.game_over_menu:
            self.game_over_menu.draw(screen)
