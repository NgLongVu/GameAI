import pygame
import math

from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BG_COLOR, NODE_RADIUS, BTN_BLUE, TEXT_COLOR, BTN_YELLOW, BTN_DARK, TEXT_LIGHT
from core.board import Board
from core.entities import Police, Thief
from core.game_state import GameState, Turn
from ui.game_over import GameOverMenu

def get_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

class GameScene:
    def __init__(self, map_path, level_name="Level 1"):
        self.level_name = level_name
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 40)
        
        self.board = Board(map_path)
        self.police_list = [Police(n) for n in self.board.start_police]
        self.thief = Thief(self.board.start_thief)
        
        self.game_state = GameState(self.board, self.police_list, self.thief)
        self.game_state.turn_start_state_freeze = self.game_state._capture_freeze_state()
        
        # UI Rects
        self.undo_rect = pygame.Rect(100, 720, 150, 50)
        self.freeze_rect = pygame.Rect(350, 720, 150, 50)
        
        # UI Setup for Top Bar
        self.btn_settings = {'pos': (55, 55), 'r': 25}
        self.btn_replay = {'pos': (115, 55), 'r': 25}
        self.btn_home = {'pos': (55, 115), 'r': 25}
        self.coins_rect = pygame.Rect(WINDOW_WIDTH - 140, 30, 120, 50)
        
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
                        self.game_state.undo()
                        self.game_state.history = []
                        self.game_state.turn_start_state_freeze = self.game_state._capture_freeze_state()
                        continue
                        
                    if self.freeze_rect.collidepoint(mouse_pos) and self.game_state.freeze_available:
                        self.game_state.use_freeze()
                        continue
                        
                if self.game_state.turn == Turn.POLICE and not self.game_state.is_animating():
                    moved = False
                    if self.game_state.selected_police:
                        for neighbor in self.game_state.selected_police.current_node.neighbors:
                            if get_distance((neighbor.x, neighbor.y), mouse_pos) < NODE_RADIUS * 1.5:
                                occupied = any(p.current_node == neighbor for p in self.police_list) or (neighbor == self.thief.current_node)
                                if not occupied:
                                    self.game_state.process_police_move(neighbor)
                                    moved = True
                                break
                    if moved: continue
                    
                    selected = False
                    for p in self.police_list:
                        if get_distance((p.current_node.x, p.current_node.y), mouse_pos) < p.radius * 1.5:
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
                self.game_over_menu = GameOverMenu(is_win=True)
            elif self.game_state.turn == Turn.GAME_OVER_THIEF_WIN:
                self.game_over_menu = GameOverMenu(is_win=False)

    def draw(self, screen):
        selectable_nodes = []
        if self.game_state.turn == Turn.POLICE and not self.game_state.is_animating():
            if self.game_state.selected_police:
                selectable_nodes = self.game_state.selected_police.current_node.neighbors
                
        self.board.draw(screen, selectable_nodes=selectable_nodes)
        
        for p in self.police_list:
            if p == self.game_state.selected_police:
                pygame.draw.circle(screen, (255, 255, 100), (int(p.visual_x), int(p.visual_y)), p.radius + 5)
            p.draw(screen)
            
        self.thief.draw(screen)

        # Draw Top Bar Elements
        # 1. Settings Button (Blue)
        sx, sy = self.btn_settings['pos']
        sr = self.btn_settings['r']
        pygame.draw.circle(screen, BTN_BLUE, (sx, sy), sr)
        pygame.draw.circle(screen, (0,0,0), (sx, sy), sr, width=2)
        pygame.draw.circle(screen, (0,0,0), (sx, sy), sr//2, width=3) # gear
        
        # 2. Replay Button (Yellow)
        rx, ry = self.btn_replay['pos']
        pygame.draw.circle(screen, BTN_YELLOW, (rx, ry), sr)
        pygame.draw.circle(screen, (0,0,0), (rx, ry), sr, width=2)
        pygame.draw.circle(screen, (0,0,0), (rx, ry), 10, width=2)
        pygame.draw.polygon(screen, (0,0,0), [(rx, ry-10), (rx-6, ry-5), (rx, ry-2)]) # arrow
        pygame.draw.polygon(screen, (0,0,0), [(rx-3, ry-4), (rx-3, ry+4), (rx+5, ry)]) # play
        
        # 3. Home Button (Blue)
        hx, hy = self.btn_home['pos']
        pygame.draw.circle(screen, BTN_BLUE, (hx, hy), sr)
        pygame.draw.circle(screen, (0,0,0), (hx, hy), sr, width=2)
        pygame.draw.polygon(screen, (0,0,0), [
            (hx, hy - 10), (hx - 10, hy), (hx - 6, hy), (hx - 6, hy + 8),
            (hx + 6, hy + 8), (hx + 6, hy), (hx + 10, hy)
        ])
        
        # 4. Level Text
        title_font = pygame.font.SysFont(None, 36, bold=True)
        level_txt = title_font.render(self.level_name.upper(), True, TEXT_COLOR)
        screen.blit(level_txt, (WINDOW_WIDTH//2 - level_txt.get_width()//2, 50))
        
        # 5. Coins Box
        pygame.draw.rect(screen, BTN_DARK, self.coins_rect, border_radius=25)
        # Gold star
        pygame.draw.circle(screen, (255, 215, 0), (self.coins_rect.x + 30, self.coins_rect.centery), 10)
        ctext = self.font.render("50", True, TEXT_LIGHT)
        screen.blit(ctext, (self.coins_rect.centerx - ctext.get_width()//2 + 10, self.coins_rect.centery - ctext.get_height()//2))
        
        # Turn/Status Text
        status_text = "Police Turn"
        color = (0, 0, 200)
        if self.game_state.turn == Turn.THIEF:
            status_text = "Thief Turn - Thinking..."
            color = (100, 100, 100)
        elif self.game_state.turn == Turn.GAME_OVER_THIEF_WIN:
            status_text = "GAME OVER - THIEF ESCAPED!"
            color = (200, 0, 0)
        elif self.game_state.turn == Turn.GAME_OVER_POLICE_WIN:
            status_text = "YOU WIN! THIEF TRAPPED!"
            color = (0, 200, 0)
            
        if self.game_state.is_thief_frozen:
            status_text += " [THIEF FROZEN]"
            color = (0, 200, 255)

        txt_surf = self.title_font.render(status_text, True, color)
        screen.blit(txt_surf, (WINDOW_WIDTH//2 - txt_surf.get_width()//2, 80))

        if self.game_state.turn in [Turn.POLICE, Turn.THIEF]:
            undo_color = (150, 150, 150) if not self.game_state.can_undo() else (200, 200, 250)
            pygame.draw.rect(screen, undo_color, self.undo_rect, border_radius=10)
            utxt = self.font.render("UNDO", True, (0,0,0))
            screen.blit(utxt, (self.undo_rect.centerx - utxt.get_width()//2, self.undo_rect.centery - utxt.get_height()//2))

            freeze_color = (150, 150, 150) if not self.game_state.freeze_available else (100, 255, 255)
            pygame.draw.rect(screen, freeze_color, self.freeze_rect, border_radius=10)
            ftxt = self.font.render("FREEZE", True, (0,0,0))
            screen.blit(ftxt, (self.freeze_rect.centerx - ftxt.get_width()//2, self.freeze_rect.centery - ftxt.get_height()//2))
            
        if self.game_over_menu:
            self.game_over_menu.draw(screen)
