"""
Point d'entrée principal du jeu StickFight.
Gère la boucle principale et les transitions entre écrans.
"""

import pygame
import config
from ui.menu import MenuScreen 
from game.game_screen import GameScreen


def main():
    """Fonction principale du jeu."""
    # Initialiser pygame
    pygame.init()
    pygame.display.set_caption("StickFight")
    
    # Créer l'écran
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Créer les écrans
    menu_screen = MenuScreen(screen)
    game_screen = GameScreen(screen)

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
        elif current_state == config.STATE_GAME:
            current_state = game_screen.draw(events, clock.get_time() / 1000.0)

        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(config.FPS)

    # Quitter
    pygame.quit()


if __name__ == "__main__":
    main()
