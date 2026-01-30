"""
Gestion de l'écran du menu principal.
"""

import pygame
from ui.button import Button
import config


class MenuScreen:
    """Représente l'écran du menu principal."""
    
    def __init__(self, screen):
        """
        Initialise le menu.
        
        Args:
            screen (pygame.Surface): La surface d'affichage principale
        """
        self.screen = screen
        self._load_assets()
        self._create_buttons()

    def _load_assets(self):
        """Charge toutes les images nécessaires pour le menu."""
        # Charger les images
        self.background_image = pygame.image.load(config.BG_PATH)
        
        # Créer les rectangles pour le positionnement
        self.background_rect = self.background_image.get_rect()


    def _create_buttons(self):
        """Crée les boutons du menu."""
        # Charger les images des boutons
        bot_btn_image = pygame.image.load(config.BOT_BTN_PATH)
        settings_btn_image = pygame.image.load(config.SETTINGS_BTN_PATH)
        quit_btn_image = pygame.image.load(config.CLOSE_BTN_PATH)

        # Calculer les dimensions de chaque bouton
        bot_width = int(bot_btn_image.get_width() * config.BUTTON_SCALE)
        bot_height = int(bot_btn_image.get_height() * config.BUTTON_SCALE)
        
        settings_width = int(settings_btn_image.get_width() * config.BUTTON_SCALE)
        settings_height = int(settings_btn_image.get_height() * config.BUTTON_SCALE)
        
        quit_width = int(quit_btn_image.get_width() * config.BUTTON_SCALE)
        quit_height = int(quit_btn_image.get_height() * config.BUTTON_SCALE)

        # Créer les boutons en colonne centrée
        center_x = self.screen.get_width() / 2
        center_y = self.screen.get_height() / 1.75

        # Premier bouton (Bot)
        self.bot_button = Button(
            center_x - bot_width / 2,
            center_y - bot_height - config.BUTTON_OFFSET_Y,
            bot_btn_image,
            config.BUTTON_SCALE
        )

        # Deuxième bouton (Settings)
        self.settings_button = Button(
            center_x - settings_width / 2,
            center_y,
            settings_btn_image,
            config.BUTTON_SCALE
        )

        # Troisième bouton (Quit)
        self.quit_button = Button(
            center_x - quit_width / 2,
            center_y + quit_height + config.BUTTON_OFFSET_Y,
            quit_btn_image,
            config.BUTTON_SCALE
        )

    def draw(self):
        """
        Dessine le menu et gère les interactions.
        
        Returns:
            str: L'état suivant ("menu", "game", ou "quit")
        """
        # Remplir l'écran de noir
        self.screen.fill(config.COLOR_BLACK)
        
        # Afficher le fond
        self.screen.blit(self.background_image, self.background_rect)

        # Gérer les boutons
        if self.bot_button.draw(self.screen):
            return config.STATE_GAME
        
        if self.settings_button.draw(self.screen):
            print("SETTINGS - À implémenter")
        
        if self.quit_button.draw(self.screen):
            return config.STATE_QUIT
        
        return config.STATE_MENU
