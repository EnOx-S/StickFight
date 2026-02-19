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
SETTINGS_PATH = ASSETS_PATH + "settings/background.png"
AUDIO_BTN_PATH = ASSETS_PATH + "settings/Audio.png"
CONTROLES_BTN_PATH = ASSETS_PATH + "settings/Controles.png"
CREDIT_BTN_PATH = ASSETS_PATH + "settings/Credit.png"
GAME_BG_PATH = ASSETS_PATH + "game/background/1.png"
HUD_EMPTY_BAR_PATH = ASSETS_PATH + "game/hud/empty.png"
HUD_FULL_BAR_PATH = ASSETS_PATH + "game/hud/full.png"
KO_IMAGE_PATH = ASSETS_PATH + "game/hud/ko.png"
BOT_BTN_PATH = ASSETS_PATH + "main_screen/play.png"
SETTINGS_BTN_PATH = ASSETS_PATH + "main_screen/settings.png"
CLOSE_BTN_PATH = ASSETS_PATH + "main_screen/quit.png"

# États de l'écran
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_SETTINGS = "settings"
STATE_MAP_SELECT = "map_select"
STATE_QUIT = "quit"

# Dimensions des boutons
BUTTON_SCALE = 0.5
BIG_BUTTON_SCALE = 0.9
BUTTON_SPACING = 20
BUTTON_OFFSET_Y = 80

# HUD
# Résolution de référence
BASE_SCREEN_WIDTH = 1280

# HUD responsive
HUD_SCALE = 1.0

HUD_MARGIN_X_RATIO = 0.105
HUD_MARGIN_Y_RATIO = 0.075


# Combat
PLAYER_ATTACK_RANGE = 140
PLAYER_ATTACK_DAMAGE = 5
PLAYER_ATTACK_Y_TOLERANCE = 50
PLAYER_KICK_RANGE = 120
PLAYER_KICK_DAMAGE = 7.5
PLAYER_KICK_Y_TOLERANCE = 60
PLAYER_KICK_KNOCKBACK_DISTANCE = 220
PLAYER_KICK_COOLDOWN = 0.65
PLAYER_KICK_MISS_STUN = 0.45
HITS_FOR_KNOCKBACK = 3
KNOCKBACK_DISTANCE = 120
KNOCKBACK_SPEED = 14
PLAYER_JUMP_SPEED = 20
PLAYER_GRAVITY = 1.1
# Parry
PARRY_STUN = 0.5
PARRY_MAX_BLOCKS = 3
PARRY_COOLDOWN = 1.0
PARRY_BREAK_STUN = 0.6

import pygame

KEY_BINDINGS = {
    "left": pygame.K_q,
    "right": pygame.K_d,
    "jump": pygame.K_SPACE,
    "attack": pygame.K_e,
    "kick": pygame.K_r,
}