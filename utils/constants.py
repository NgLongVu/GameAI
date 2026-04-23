# Screen settings
# Screen settings (These will be updated dynamically in main.py)
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 900
FPS = 60

# Base Colors
BG_COLOR = (245, 240, 225)  # Light beige (base bg)
MENU_BG_COLOR = (245, 235, 215) # Very similar tone for main menu
DARK_OVERLAY_COLOR = (40, 40, 35, 220) # Semi-transparent for Level Select

# Game Colors
LINE_COLOR = (90, 100, 180)
NODE_COLOR = (120, 130, 200)
NODE_BORDER_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 100)
TEXT_COLOR = (40, 40, 40)
EXIT_COLOR = (255, 80, 80)
EXIT_FILL = (255, 255, 255)

# UI Colors (Menu)
BTN_BLUE = (120, 195, 245)
BTN_DARK_BLUE = (15, 45, 85)
BTN_LOCKED = (200, 185, 140)
BTN_DARK = (60, 60, 60)
TEXT_LIGHT = (255, 255, 255)

# UI Colors (Settings Popup)
POPUP_HEADER = (255, 215, 80)
POPUP_BODY = (245, 245, 245)
TOGGLE_ON = (140, 200, 80)
TOGGLE_OFF = (200, 200, 200)

# GameOver Colors
BTN_YELLOW = (255, 215, 80)
BTN_GREEN = (150, 220, 120)
TEXT_ORANGE = (240, 130, 40)

# Game Mechanics
LERP_SPEED = 0.15
NODE_RADIUS = 22
EXIT_SIZE = 46

# Map files (ordered by level index)
MAP_PATHS = [
    'data/map_1.json',
    'data/map_2.json',
    'data/map_3.json',
    'data/map_4.json',
    'data/map_5.json',
    'data/map_6.json',
    'data/map_7.json',
    'data/map_8.json'
]
