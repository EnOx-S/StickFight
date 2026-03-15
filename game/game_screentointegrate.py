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
        )        # Timer
        self.elapsed_time = 0.0
        self.font = pygame.font.Font(None, 60)  # Police par défaut de pygame
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
        charge_full = pygame.image.load(config.HUD_FULL_CHARGE_PATH).convert_alpha()
        charge_empty = pygame.image.load(config.HUD_EMPTY_CHARGE_PATH).convert_alpha()
        charge_full = pygame.transform.scale(charge_full,(int(self.screen.get_width()*0.2), int(self.screen.get_height()*0.2)))
        charge_empty = pygame.transform.scale(charge_empty, (int(self.screen.get_width()*0.2), int(self.screen.get_height()*0.2)))

        screen_ratio = self.screen.get_width() / config.BASE_SCREEN_WIDTH
        hud_scale = config.HUD_SCALE * screen_ratio

        scaled_width = int(base_full.get_width() * hud_scale)
        scaled_height = int(base_full.get_height() * hud_scale)
        charge_scaled_width = int(charge_full.get_width() * hud_scale)
        charge_scaled_height = int(charge_full.get_height() * hud_scale)


        self.health_empty_image = pygame.transform.scale(
            base_empty, (scaled_width, scaled_height)
        )
        self.health_full_image = pygame.transform.scale(
            base_full, (scaled_width, scaled_height)
        )

        self.charge_empty_image = pygame.transform.scale(
            charge_empty, (charge_scaled_width, charge_scaled_height)
        )
        self.charge_full_image = pygame.transform.scale(
            charge_full, (charge_scaled_width, charge_scaled_height)
        )
        self.charge_empty_image_flipped = pygame.transform.flip(self.charge_empty_image, True, False)
        self.charge_full_image_flipped = pygame.transform.flip(self.charge_full_image, True, False)


        self.health_bar_width = scaled_width
        self.health_bar_height = scaled_height
        self.charge_bar_height = charge_scaled_height 
        self.charge_bar_width = charge_scaled_width

        self.ko_image = pygame.image.load(config.KO_IMAGE_PATH).convert_alpha()

        # Taille finale du KO (40% largeur écran)
        ko_target_width = int(self.screen.get_width() * 0.55)
        ratio = ko_target_width / self.ko_image.get_width()
        ko_target_height = int(self.ko_image.get_height() * ratio)

        self.ko_final_size = (ko_target_width, ko_target_height)

        self.ko_active = False
        self.ko_timer = 0.0

    def _draw_timer(self):
        """
        Affiche le temps écoulé au centre haut de l'écran.
        """
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        time_text = f"{minutes:02d}:{seconds:02d}"
        
        text_surface = self.font.render(time_text, True, config.COLOR_WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.screen.get_width() // 2
        text_rect.top = int(self.screen.get_height() * 0.02)
        
        self.screen.blit(text_surface, text_rect)


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
        
        
    
    def _draw_charge_bar(self, x, y, charge, max_charge, anchor_right=False, is_bot=False):
        """
        Affiche la barre vide complete et rogne la barre pleine selon la charge.
        """
        c_bar_width = self.charge_bar_width
        c_bar_height = self.charge_bar_height

        if max_charge <= 0:
            charge_ratio = 0.0
        else:
            charge_ratio = max(0.0, min(1.0, charge / max_charge))

        charge_width = int(c_bar_width * charge_ratio)

        empty_image = self.charge_empty_image_flipped if is_bot else self.charge_empty_image
        full_image = self.charge_full_image_flipped if is_bot else self.charge_full_image

        self.screen.blit(empty_image, (x, y))

        if charge_width <= 0:
            return

        if anchor_right:
            source_x = c_bar_width - charge_width
            source_rect = pygame.Rect(source_x, 0, charge_width, c_bar_height)
            target_x = x + source_x
            self.screen.blit(full_image, (target_x, y), source_rect)
        else:
            source_rect = pygame.Rect(0, 0, charge_width, c_bar_height)
            self.screen.blit(full_image, (x, y), source_rect)

    def draw(self, events, delta_time):
        """
        Dessine l'ecran de jeu et gere les interactions.

        Args:
            events (list): Liste des evenements pygame

        Returns:
            str: L'etat suivant ("game" ou "menu")
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.reset()
                return config.STATE_MENU

        self.screen.fill(config.COLOR_BLACK)
        self.screen.blit(self.background_image, self.background_rect)

        keys = pygame.key.get_pressed()

        if self.player.pos_x < self.bot.pos_x:
            self.player.facing_dir = 1
            self.bot.facing_dir = -1
        else:
            self.player.facing_dir = -1
            self.bot.facing_dir = 1

        if not self.ko_active:
            self.player.handle_movement(keys)
        self.player.update(delta_time)

        self.bot.handle_movement()
        self.bot.update(delta_time)

        self.bot.try_hit_target(self.player)
        # Detection de coup type "raycast" en X depuis le joueur vers le bot.
        self.player.try_hit_target(self.bot)

        self.player.draw(self.screen)
        self.bot.draw(self.screen)

        if not self.ko_active and (self.player.health <= 0 or self.bot.health <= 0):
            self.ko_active = True
            self.ko_timer = 0.0
        if self.ko_active:
            self._draw_ko(delta_time)

        margin_x = int(self.screen.get_width() * config.HUD_MARGIN_X_RATIO)
        margin_y = int(self.screen.get_height() * config.HUD_MARGIN_Y_RATIO)

        bar_width = self.health_bar_width
        bar_height = self.health_bar_height
        c_bar_height = self.charge_bar_height
        c_bar_width = self.charge_bar_width


        player_x = margin_x
        player_y = margin_y

        bot_x = self.screen.get_width() - bar_width - margin_x
        bot_y = margin_y
        
        player_x = max(0, min(player_x, self.screen.get_width() - bar_width))
        bot_x = max(0, min(bot_x, self.screen.get_width() - bar_width))

        charge_offset = bar_height + 3
        
        # Center charge bars relative to health bars
        charge_player_x = player_x + (bar_width - c_bar_width) // 2
        charge_bot_x = bot_x + (bar_width - c_bar_width) // 2

        self._draw_health_bar(player_x, player_y, self.player.health, self.player.max_health)
        self._draw_health_bar(bot_x, bot_y, self.bot.health, self.bot.max_health, anchor_right=True)
        self._draw_charge_bar(charge_player_x, player_y + charge_offset, self.player.charge, self.player.max_charge)
        self._draw_charge_bar(charge_bot_x, bot_y + charge_offset, self.bot.charge, self.bot.max_charge, anchor_right=True, is_bot=True)        
        # Afficher le timer
        self._draw_timer()
        
        self.elapsed_time += delta_time
        return config.STATE_GAME

    def _draw_ko(self, delta_time):
        self.ko_timer += delta_time

        # Durée animation
        anim_duration = 0.4

        t = min(self.ko_timer / anim_duration, 1.0)

        # Courbe violente (ease out back)
        overshoot = 1.3
        scale = (
            1 +
            (overshoot - 1) * (1 - t) * pygame.math.lerp(1, 0, t)
        )

        base_w, base_h = self.ko_final_size
        w = int(base_w * scale)
        h = int(base_h * scale)

        ko_scaled = pygame.transform.scale(self.ko_image, (w, h))

        x = self.screen.get_width() // 2 - w // 2
        y = self.screen.get_height() // 2 - h // 2

        # petit shake
        shake = int(8 * (1 - t))
        x += pygame.time.get_ticks() % 2 * shake - shake // 2

        self.screen.blit(ko_scaled, (x, y))

    def reset(self):
        """Remet le jeu à zéro."""
        self.player.reset()
        self.bot.reset(target=self.player)
        self.ko_active = False
        self.ko_timer = 0.0
        self.elapsed_time = 0.0
