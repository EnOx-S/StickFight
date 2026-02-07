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
GAME_BG_PATH = ASSETS_PATH + "game/background/soulsociety.png"
HUD_EMPTY_BAR_PATH = ASSETS_PATH + "game/hud/empty.png"
HUD_FULL_BAR_PATH = ASSETS_PATH + "game/hud/full.png"
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

# HUD
HUD_MARGIN_X = 30
HUD_MARGIN_Y = 30
HUD_SCALE = 2.0

# Combat
PLAYER_ATTACK_RANGE = 140
PLAYER_ATTACK_DAMAGE = 5
PLAYER_ATTACK_Y_TOLERANCE = 50
PLAYER_KICK_RANGE = 170
PLAYER_KICK_DAMAGE = 10
PLAYER_KICK_Y_TOLERANCE = 60
PLAYER_KICK_KNOCKBACK_DISTANCE = 220
PLAYER_KICK_COOLDOWN = 0.45
PLAYER_KICK_MISS_STUN = 0.3
HITS_FOR_KNOCKBACK = 3
KNOCKBACK_DISTANCE = 120
KNOCKBACK_SPEED = 14
PLAYER_JUMP_SPEED = 20
PLAYER_GRAVITY = 1.1
