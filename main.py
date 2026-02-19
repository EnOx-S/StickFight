"""
Point d'entrée principal du jeu StickFight.
Gère la boucle principale et les transitions entre écrans.
"""

import pygame
import config
from ui.menu import MenuScreen
from ui.map_select import MapSelectScreen
from ui.settings import SettingsScreen
from game.game_screen import GameScreen


def main():
    """Fonction principale du jeu."""
    # Initialiser pygame
    pygame.init()
    # Initialiser le mixer audio si possible (silencieux en cas d'erreur)
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except Exception:
        print("Warning: audio mixer failed to initialize. Sounds will be disabled.")
    pygame.display.set_caption("StickFight")
    
    # Créer l'écran
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Créer les écrans
    menu_screen = MenuScreen(screen)
    map_select = None
    game_screen = None
    settings_screen = SettingsScreen(screen)

    # État initial
    current_state = config.STATE_MENU
    running = True

    # Boucle principale
    while running:
        # Gérer les événements
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Gérer les états
        if current_state == config.STATE_MENU:
            current_state = menu_screen.draw()
            if current_state == config.STATE_QUIT:
                running = False
        elif current_state == config.STATE_SETTINGS:
            # Réinitialiser le zoom à chaque entrée sur settings
            if 'previous_state' in locals() and previous_state != config.STATE_SETTINGS:
                settings_screen.zoom_factor = 1.0
            previous_state = current_state
            current_state = settings_screen.draw(events)
        elif current_state == config.STATE_MAP_SELECT:
            # Créer l'écran de sélection si nécessaire
            if map_select is None:
                map_select = MapSelectScreen(screen)
            result = map_select.draw(events)
            # Si l'utilisateur choisi une carte, result est (STATE_GAME, path)
            if isinstance(result, tuple) and result[0] == config.STATE_GAME:
                _, bg_path = result
                game_screen = GameScreen(screen, background_path=bg_path)
                current_state = config.STATE_GAME
            else:
                # result peut être STATE_MENU ou STATE_MAP_SELECT
                current_state = result
                if current_state == config.STATE_MENU:
                    map_select = None
        elif current_state == config.STATE_GAME:
            if game_screen is None:
                # fallback au cas improbable où on entre ici sans game_screen
                game_screen = GameScreen(screen)
            current_state = game_screen.draw(events, clock.get_time() / 1000.0)

        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(config.FPS)

    # Quitter
    pygame.quit()


if __name__ == "__main__":
    main()
