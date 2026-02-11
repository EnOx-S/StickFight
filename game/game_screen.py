"""
Gestion de l'ecran de jeu.
"""

import pygame
import config
from game.player import Player
from game.bot import Bot


class GameScreen:
    """Represente l'ecran de jeu."""

    def __init__(self, screen):
        """
        Initialise l'ecran de jeu.

        Args:
            screen (pygame.Surface): La surface d'affichage principale
        """
        self.screen = screen
        self._load_assets()
        self.player = Player(
            x=screen.get_width() * 0.25,
            y=screen.get_height() // 2
        )
        self.bot = Bot(
            x=screen.get_width() * 0.5,
            y=screen.get_height() // 2, target=self.player
        )

    def _load_assets(self):
        """Charge toutes les images necessaires pour le jeu."""
        game_bg_image = pygame.image.load(config.GAME_BG_PATH)
        self.background_image = pygame.transform.scale(
            game_bg_image,
            (self.screen.get_width(), self.screen.get_height())
        )
        self.background_rect = self.background_image.get_rect()

        base_empty = pygame.image.load(config.HUD_EMPTY_BAR_PATH).convert_alpha()
        base_full = pygame.image.load(config.HUD_FULL_BAR_PATH).convert_alpha()

        screen_ratio = self.screen.get_width() / config.BASE_SCREEN_WIDTH
        hud_scale = config.HUD_SCALE * screen_ratio

        scaled_width = int(base_full.get_width() * hud_scale)
        scaled_height = int(base_full.get_height() * hud_scale)

        self.health_empty_image = pygame.transform.scale(
            base_empty, (scaled_width, scaled_height)
        )
        self.health_full_image = pygame.transform.scale(
            base_full, (scaled_width, scaled_height)
        )

        self.health_bar_width = scaled_width
        self.health_bar_height = scaled_height

    def _draw_health_bar(self, x, y, health, max_health, anchor_right=False):
        """
        Affiche la barre vide complete et rogne la barre pleine selon la vie.
        """
        bar_width = self.health_bar_width
        bar_height = self.health_bar_height

        if max_health <= 0:
            health_ratio = 0.0
        else:
            health_ratio = max(0.0, min(1.0, health / max_health))

        health_width = int(bar_width * health_ratio)

        self.screen.blit(self.health_empty_image, (x, y))

        if health_width <= 0:
            return

        if anchor_right:
            source_x = bar_width - health_width
            source_rect = pygame.Rect(source_x, 0, health_width, bar_height)
            target_x = x + source_x
            self.screen.blit(self.health_full_image, (target_x, y), source_rect)
        else:
            source_rect = pygame.Rect(0, 0, health_width, bar_height)
            self.screen.blit(self.health_full_image, (x, y), source_rect)


    def draw(self, events, delta_time):
        """
        Dessine l'ecran de jeu et gere les interactions.

        Args:
            events (list): Liste des evenements pygame

        Returns:
            str: L'etat suivant ("game" ou "menu")
        """
        self.screen.fill(config.COLOR_BLACK)
        self.screen.blit(self.background_image, self.background_rect)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return config.STATE_MENU

        keys = pygame.key.get_pressed()

        if self.player.pos_x < self.bot.pos_x:
            self.player.facing_dir = 1
            self.bot.facing_dir = -1
        else:
            self.player.facing_dir = -1
            self.bot.facing_dir = 1

        self.player.handle_movement(keys)
        self.player.update(delta_time)

        self.bot.handle_movement()
        self.bot.update(delta_time)

        self.bot.try_hit_target(self.player)
        # Detection de coup type "raycast" en X depuis le joueur vers le bot.
        self.player.try_hit_target(self.bot)

        self.player.draw(self.screen)
        self.bot.draw(self.screen)

        margin_x = int(self.screen.get_width() * config.HUD_MARGIN_X_RATIO)
        margin_y = int(self.screen.get_height() * config.HUD_MARGIN_Y_RATIO)

        bar_width = self.health_bar_width
        bar_height = self.health_bar_height

        player_x = margin_x
        player_y = margin_y

        bot_x = self.screen.get_width() - bar_width - margin_x
        bot_y = margin_y

        player_x = max(0, min(player_x, self.screen.get_width() - bar_width))
        bot_x = max(0, min(bot_x, self.screen.get_width() - bar_width))

        self._draw_health_bar(player_x, player_y, self.player.health, self.player.max_health)
        self._draw_health_bar(bot_x, bot_y, self.bot.health, self.bot.max_health, anchor_right=True)

        return config.STATE_GAME
