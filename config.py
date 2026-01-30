"""
Configuration centralisée du jeu.
Contient toutes les constantes utilisées dans l'application.
"""

# Dimensions de l'écran
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# Couleurs (format RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Chemins des assets
ASSETS_PATH = "assets/images/"
BG_PATH = ASSETS_PATH + "main_screen/background.png"
GAME_BG_PATH = ASSETS_PATH + "game_background/soulsociety.png"
BOT_BTN_PATH = ASSETS_PATH + "main_screen/play.png"
SETTINGS_BTN_PATH = ASSETS_PATH + "main_screen/settings.png"
CLOSE_BTN_PATH = ASSETS_PATH + "main_screen/quit.png"

# États de l'écran
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_QUIT = "quit"

# Dimensions des boutons
BUTTON_SCALE = 0.5
BUTTON_SPACING = 20
BUTTON_OFFSET_Y = 80
