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
        
        # Animation variables
        self.animation_time = 0.0
        self.animation_duration = 2.0  # Durée en secondes
        self.zoom_start = 1.5  # Zoom initial (dézoomé)
        self.zoom_end = 1.0  # Zoom final (100%)

    def _load_assets(self):
        """Charge toutes les images nécessaires pour le menu."""
        # Charger les images
        self.background_image = pygame.image.load(config.BG_PATH)
        
        # Créer les rectangles pour le positionnement
        self.background_rect = self.background_image.get_rect()
        self.background_rect.center = (
            self.screen.get_width() / 2,
            self.screen.get_height() / 2
        )
        
        # Stocker l'image originale pour le zoom
        self.background_image_original = self.background_image.copy()


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

    def draw(self, delta_time=0.0):
        """
        Dessine le menu et gère les interactions.
        
        Args:
            delta_time (float): Temps écoulé depuis la dernière frame en secondes
        
        Returns:
            str: L'état suivant ("menu", "game", ou "quit")
        """
        # Mettre à jour l'animation
        if self.animation_time < self.animation_duration:
            self.animation_time += delta_time
        
        # Remplir l'écran de noir
        self.screen.fill(config.COLOR_BLACK)
        
        # Calculer le facteur de zoom (interpolation linéaire)
        zoom_progress = min(self.animation_time / self.animation_duration, 1.0)
        current_zoom = self.zoom_start + (self.zoom_end - self.zoom_start) * zoom_progress
        
        # Appliquer le zoom au fond
        zoomed_width = int(self.background_image_original.get_width() / current_zoom)
        zoomed_height = int(self.background_image_original.get_height() / current_zoom)
        zoomed_image = pygame.transform.scale(self.background_image_original, (zoomed_width, zoomed_height))
        
        # Centrer l'image zoomée
        zoomed_rect = zoomed_image.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2)
        )
        
        # Afficher le fond zoomé
        self.screen.blit(zoomed_image, zoomed_rect)

        # Calculer l'alpha pour les boutons (apparition progressive pendant le zoom - très transparente au début)
        buttons_progress = min(self.animation_time / self.animation_duration, 1.0)
        # Utiliser une courbe d'easing pour que ce soit plus transparent au début
        eased_progress = buttons_progress ** 3  # Progression cubique pour effet plus progressif
        alpha = int(255 * eased_progress)
        
        # Afficher les boutons avec alpha
        bot_clicked = self.bot_button.draw(self.screen, alpha)
        settings_clicked = self.settings_button.draw(self.screen, alpha)
        quit_clicked = self.quit_button.draw(self.screen, alpha)
        
        # Gérer les clics des boutons - toujours vérifier mais seulement retourner après l'anim
        if bot_clicked and buttons_progress >= 1.0:
            return config.STATE_MAP_SELECT
        
        if settings_clicked and buttons_progress >= 1.0:
            return config.STATE_SETTINGS
        
        if quit_clicked and buttons_progress >= 1.0:
            return config.STATE_QUIT
        
        return config.STATE_MENU
