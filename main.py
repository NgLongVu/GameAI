import pygame
import sys

from utils.constants import FPS, MAP_PATHS
from utils.audio_manager import AudioManager
from utils.save_manager import SaveManager

import utils.constants as const

def main():
    pygame.init()
    
    # --- Dynamic Resolution Detection ---
    info = pygame.display.Info()
    # Subtracting ~120px for taskbar and window headers
    target_h = min(900, info.current_h - 120)
    # Target aspect ratio - slightly wider as requested
    target_w = int(target_h * 0.65) 
    
    # Update global constants to a safe base resolution
    const.WINDOW_WIDTH = target_w
    const.WINDOW_HEIGHT = target_h
    
    # Use ONLY RESIZABLE (removed SCALED to allow true responsive layout)
    screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Graph Pursuit - Catch The Thief")
    clock = pygame.time.Clock()

    # Audio
    audio = AudioManager()
    audio.play_music()
    
    # Save Manager
    save_manager = SaveManager()

    # Pre-load menus
    from ui.main_menu import MainMenu
    from ui.level_select import LevelSelectMenu
    from ui.settings_menu import SettingsMenu
    from core.game_scene import GameScene
    
    main_menu = MainMenu()
    level_select_menu = LevelSelectMenu()
    settings_menu = SettingsMenu()
    
    game_scene = None
    current_level_idx = 0
    level_rewarded = False
    
    app_state = "MAIN_MENU"
    prev_state = "MAIN_MENU"

    running = True
    while running:
        dt = clock.tick(FPS)
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # --- HANDLE WINDOW RESIZE ---
            if event.type == pygame.VIDEORESIZE:
                const.WINDOW_WIDTH, const.WINDOW_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT), pygame.RESIZABLE)
                # Refresh layouts of all active components
                main_menu = MainMenu() # Re-init to recalc rects
                level_select_menu = LevelSelectMenu()
                settings_menu = SettingsMenu()
                if game_scene:
                    # Capture current state before re-init to preserve game progress
                    old_state = game_scene.game_state
                    game_scene = GameScene(MAP_PATHS[current_level_idx], level_name=f"Level {current_level_idx + 1}")
                    # Transfer entities and state back to the new layout
                    game_scene.game_state = old_state
                    game_scene.board = old_state.board
                    game_scene.board._normalize_map_coordinates() # Recalc node positions
            
            if app_state == "SETTINGS_MENU":
                if event.type == pygame.MOUSEMOTION:
                    settings_menu.handle_drag(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    settings_menu.handle_release()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                # State Routing
                if app_state == "MAIN_MENU":
                    action = main_menu.handle_click(mouse_pos)
                    if action == "PLAY_LATEST":
                        audio.play_sfx('click')
                        # Smart Play: Start from the highest unlocked level
                        current_level_idx = max(0, save_manager.get_max_level() - 1)
                        if current_level_idx >= len(MAP_PATHS):
                            current_level_idx = len(MAP_PATHS) - 1
                        
                        level_rewarded = False
                        game_scene = GameScene(MAP_PATHS[current_level_idx], 
                                              level_name=f"Level {current_level_idx + 1}")
                        app_state = "PLAYING"
                    elif action == "OPEN_LEVEL_SELECT":
                        audio.play_sfx('click')
                        app_state = "LEVEL_SELECT"
                    elif action == "OPEN_SETTINGS":
                        audio.play_sfx('click')
                        prev_state = app_state
                        app_state = "SETTINGS_MENU"
                        
                elif app_state == "LEVEL_SELECT":
                    action = level_select_menu.handle_click(mouse_pos)
                    if action == "BACK_TO_MENU":
                        audio.play_sfx('click')
                        app_state = "MAIN_MENU"
                    elif action and action.startswith("PLAY_LEVEL_"):
                        audio.play_sfx('click')
                        lvl_idx = int(action.split("_")[-1]) - 1
                        current_level_idx = min(lvl_idx, len(MAP_PATHS) - 1)
                        level_rewarded = False
                        map_path = MAP_PATHS[current_level_idx]
                        game_scene = GameScene(map_path, level_name=f"Level {current_level_idx + 1}")
                        app_state = "PLAYING"
                        
                elif app_state == "SETTINGS_MENU":
                    action = settings_menu.handle_click(mouse_pos)
                    if action == "CLOSE_SETTINGS":
                        audio.play_sfx('click')
                        app_state = prev_state

        # Dedicated logic updates
        if app_state == "PLAYING":
            if game_scene:
                action = game_scene.handle_events(events)
                if action == "BACK_TO_MENU" or action == "LEVELS":
                    audio.play_sfx('click')
                    app_state = "MAIN_MENU" if action == "BACK_TO_MENU" else "LEVEL_SELECT"
                    game_scene = None # clear memory
                elif action is None:
                    status = game_scene.update()
                    if status == "POLICE_WIN" and not level_rewarded:
                        # Reward coins and unlock next level
                        save_manager.add_coins(15)
                        save_manager.unlock_level(current_level_idx + 2)
                        level_rewarded = True
                elif action in ["REPLAY", "NEXT"]:
                    audio.play_sfx('click')
                    level_rewarded = False
                    if action == "NEXT":
                        current_level_idx = min(current_level_idx + 1, len(MAP_PATHS) - 1)
                    game_scene = GameScene(MAP_PATHS[current_level_idx], level_name=f"Level {current_level_idx + 1}")
                elif action == "OPEN_SETTINGS":
                    audio.play_sfx('click')
                    prev_state = app_state
                    app_state = "SETTINGS_MENU"


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
