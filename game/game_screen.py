"""
Gestion de l'écran de jeu.
"""

import pygame
import config
from game.player import Player

class GameScreen:
    """Représente l'écran de jeu."""
    
    def __init__(self, screen):
        """
        Initialise l'écran de jeu.
        
        Args:
            screen (pygame.Surface): La surface d'affichage principale
        """
        self.screen = screen
        self._load_assets()
        self.player = Player(
            x=screen.get_width() // 2,
            y=screen.get_height() // 2
        )

    def _load_assets(self):
        """Charge toutes les images nécessaires pour le jeu."""
        game_bg_image = pygame.image.load(config.GAME_BG_PATH)
        # Redimensionner le fond à la taille de l'écran
        self.background_image = pygame.transform.scale(
            game_bg_image,
            (self.screen.get_width(), self.screen.get_height())
        )
        self.background_rect = self.background_image.get_rect()

    def draw(self, events, delta_time):
        """
        Dessine l'écran de jeu et gère les interactions.
        
        Args:
            events (list): Liste des événements pygame
            
        Returns:
            str: L'état suivant ("game" ou "menu")
        """
        # Remplir l'écran de noir
        self.screen.fill(config.COLOR_BLACK)
        
        # Afficher le fond
        self.screen.blit(self.background_image, self.background_rect)

        # Gérer les événements
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return config.STATE_MENU
        
        keys = pygame.key.get_pressed()

        self.player.handle_movement(keys)
        self.player.update(delta_time)
        self.player.draw(self.screen)

        return config.STATE_GAME
