import pygame
import sys

from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, MAP_PATHS
from ui.main_menu import MainMenu
from ui.level_select import LevelSelectMenu
from ui.settings_menu import SettingsMenu
from core.game_scene import GameScene

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Graph Pursuit - Catch The Thief")
    clock = pygame.time.Clock()

    # Pre-load menus
    main_menu = MainMenu()
    level_select_menu = LevelSelectMenu()
    settings_menu = SettingsMenu()
    
    # Game Manager
    game_scene = None
    
    # State Machine
    # STATES: "MAIN_MENU", "LEVEL_SELECT", "PLAYING", "SETTINGS_MENU"
    app_state = "MAIN_MENU"
    prev_state = "MAIN_MENU"

    running = True
    while running:
        dt = clock.tick(FPS)
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                # State Routing
                if app_state == "MAIN_MENU":
                    action = main_menu.handle_click(mouse_pos)
                    if action == "PLAY_LEVEL_1":
                        game_scene = GameScene(MAP_PATHS[0], level_name="Level 1")
                        app_state = "PLAYING"
                    elif action == "OPEN_LEVEL_SELECT":
                        app_state = "LEVEL_SELECT"
                    elif action == "OPEN_SETTINGS":
                        prev_state = app_state
                        app_state = "SETTINGS_MENU"
                        
                elif app_state == "LEVEL_SELECT":
                    action = level_select_menu.handle_click(mouse_pos)
                    if action == "BACK_TO_MENU":
                        app_state = "MAIN_MENU"
                    elif action and action.startswith("PLAY_LEVEL_"):
                        lvl_idx = int(action.split("_")[-1]) - 1
                        map_path = MAP_PATHS[min(lvl_idx, len(MAP_PATHS) - 1)]
                        game_scene = GameScene(map_path, level_name=f"Level {lvl_idx + 1}")
                        app_state = "PLAYING"
                        
                elif app_state == "SETTINGS_MENU":
                    action = settings_menu.handle_click(mouse_pos)
                    if action == "CLOSE_SETTINGS":
                        app_state = prev_state

        # Dedicated logic updates
        if app_state == "PLAYING":
            if game_scene:
                action = game_scene.handle_events(events)
                if action == "BACK_TO_MENU" or action == "LEVELS":
                    app_state = "MAIN_MENU" if action == "BACK_TO_MENU" else "LEVEL_SELECT"
                    game_scene = None # clear memory
                elif action in ["REPLAY", "NEXT"]:
                    game_scene = GameScene(MAP_PATHS[0], level_name="Level 1")
                elif action == "OPEN_SETTINGS":
                    prev_state = app_state
                    app_state = "SETTINGS_MENU"
                elif action is None:
                    game_scene.update()

        # Rendering
        if app_state == "MAIN_MENU":
            main_menu.draw(screen)
            
        elif app_state == "SETTINGS_MENU":
            # Overlay over Previous State
            if prev_state == "MAIN_MENU":
                main_menu.draw(screen)
            elif prev_state == "PLAYING" and game_scene:
                game_scene.draw(screen)
            settings_menu.draw(screen)
            
        elif app_state == "LEVEL_SELECT":
            # Level Select is explicitly an overlay over Main Menu
            main_menu.draw(screen)
            level_select_menu.draw(screen)
            
        elif app_state == "PLAYING" and game_scene:
            game_scene.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
