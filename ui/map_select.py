"""
Écran de sélection de la carte minimaliste.

Affiche :
- fond noir
- titre responsive centré en haut
- une vignette de la carte au centre
- deux flèches (gauche/droite) pour changer la carte

Cliquer sur la vignette renvoie (config.STATE_GAME, path).
Appuyer sur ESC revient au menu.
"""

import pygame
import config
from ui.button import Button
import os


class MapSelectScreen:
    def __init__(self, screen):
        self.screen = screen
        self.maps = []  # list of (path, surface)
        self.current_index = 0
        self.left_button = None
        self.right_button = None
        self._load_maps()
        self._create_arrow_buttons()

    def _load_maps(self):
        """Recense les chemins disponibles et prépare une file de chargement.

        Les images ne sont pas chargées immédiatement pour éviter le freeze;
        elles seront chargées progressivement (une par frame) dans draw().
        """
        self.maps = []
        self._load_queue = []
        for i in range(1, 21):
            path = config.ASSETS_PATH + f"game/background/{i}.png"
            if os.path.exists(path):
                # stocke une entrée dict avec image None pour chargement ultérieur
                self.maps.append({"path": path, "img": None})
                self._load_queue.append(path)

        if not self.maps:
            self.current_index = -1

    def _process_load_queue_once(self):
        """Charge une seule image depuis la file de chargement (si présente)."""
        if not hasattr(self, "_load_queue") or not self._load_queue:
            return
        next_path = self._load_queue.pop(0)
        try:
            img = pygame.image.load(next_path).convert()
        except Exception:
            img = None
        # trouver l'entrée correspondante et assigner l'image
        for entry in self.maps:
            if entry["path"] == next_path:
                entry["img"] = img
                break

    def _make_arrow_surface(self, direction, size, color=(255, 255, 255)):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx = size // 2
        cy = size // 2
        m = int(size * 0.2)
        if direction == "left":
            points = [(cx + m, m), (cx - m, cy), (cx + m, size - m)]
        else:
            points = [(cx - m, m), (cx + m, cy), (cx - m, size - m)]
        pygame.draw.polygon(surf, color, points)
        return surf

    def _create_arrow_buttons(self):
        size = max(48, int(self.screen.get_height() * 0.12))
        left_img = self._make_arrow_surface("left", size)
        right_img = self._make_arrow_surface("right", size)
        self.left_button = Button(0, 0, left_img, 1.0)
        self.right_button = Button(0, 0, right_img, 1.0)

    def draw(self, events):
        # Aucun fond trouvé
        if self.current_index == -1:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return config.STATE_MENU
            self.screen.fill(config.COLOR_BLACK)
            font = pygame.font.SysFont(None, max(24, int(self.screen.get_width() * 0.03)))
            text = font.render("Aucune carte trouvée. Appuyez sur ESC.", True, config.COLOR_WHITE)
            tx = self.screen.get_width() // 2 - text.get_width() // 2
            ty = self.screen.get_height() // 2 - text.get_height() // 2
            self.screen.blit(text, (tx, ty))
            return config.STATE_MAP_SELECT

        # Gestion clavier et collecte du clic souris (uniquement MOUSEBUTTONDOWN)
        mouse_click_pos = None
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return config.STATE_MENU
                if event.key == pygame.K_RIGHT:
                    self.current_index = (self.current_index + 1) % len(self.maps)
                if event.key == pygame.K_LEFT:
                    self.current_index = (self.current_index - 1) % len(self.maps)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_pos = event.pos

        # Traiter un élément de la file de chargement par frame
        self._process_load_queue_once()

        # Fond noir
        self.screen.fill(config.COLOR_BLACK)

        # Titre responsive centré en haut
        title = "Sélectionnez une carte"
        font_size = max(18, min(64, int(self.screen.get_width() * 0.04)))
        font = pygame.font.SysFont(None, font_size)
        title_surf = font.render(title, True, config.COLOR_WHITE)
        tx = self.screen.get_width() // 2 - title_surf.get_width() // 2
        ty = int(self.screen.get_height() * 0.07)
        self.screen.blit(title_surf, (tx, ty))

        # Affiche la vignette centrée
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        entry = self.maps[self.current_index]
        path = entry["path"]
        img = entry["img"]

        max_w = int(self.screen.get_width() * 0.6)
        max_h = int(self.screen.get_height() * 0.6)

        if img is None:
            # placeholder pendant le chargement
            placeholder_w = int(self.screen.get_width() * 0.4)
            placeholder_h = int(self.screen.get_height() * 0.3)
            img_x = center_x - placeholder_w // 2
            img_y = center_y - placeholder_h // 2
            img_rect = pygame.Rect(img_x, img_y, placeholder_w, placeholder_h)
            pygame.draw.rect(self.screen, (40, 40, 40), img_rect)
            load_font = pygame.font.SysFont(None, max(18, int(self.screen.get_width() * 0.02)))
            load_text = load_font.render("Chargement...", True, config.COLOR_WHITE)
            lx = center_x - load_text.get_width() // 2
            ly = center_y - load_text.get_height() // 2
            self.screen.blit(load_text, (lx, ly))
            display_w = placeholder_w
            display_h = placeholder_h
        else:
            iw, ih = img.get_width(), img.get_height()
            scale = min(max_w / iw, max_h / ih)
            display_w = max(1, int(iw * scale))
            display_h = max(1, int(ih * scale))
            displayed = pygame.transform.scale(img, (display_w, display_h))
            img_x = center_x - display_w // 2
            img_y = center_y - display_h // 2
            img_rect = pygame.Rect(img_x, img_y, display_w, display_h)
            self.screen.blit(displayed, (img_x, img_y))

        # Flèches : générer surfaces à la taille appropriée et positionner boutons
        arrow_size = max(48, int(self.screen.get_height() * 0.12))
        left_img = self._make_arrow_surface("left", arrow_size)
        right_img = self._make_arrow_surface("right", arrow_size)
        self.left_button.image = left_img
        self.left_button.rect = self.left_button.image.get_rect()
        self.right_button.image = right_img
        self.right_button.rect = self.right_button.image.get_rect()

        left_x = img_x - arrow_size - 20
        right_x = img_x + display_w + 20
        arrow_y = center_y - arrow_size // 2
        self.left_button.rect.topleft = (left_x, arrow_y)
        self.right_button.rect.topleft = (right_x, arrow_y)

        # Dessine les flèches
        self.left_button.draw(self.screen)
        self.right_button.draw(self.screen)

        # Gérer le clic souris (utiliser la position du MOUSEBUTTONDOWN pour éviter le carryover)
        if mouse_click_pos:
            if img_rect.collidepoint(mouse_click_pos):
                return (config.STATE_GAME, path)
            if self.left_button.rect.collidepoint(mouse_click_pos):
                self.current_index = (self.current_index - 1) % len(self.maps)
            if self.right_button.rect.collidepoint(mouse_click_pos):
                self.current_index = (self.current_index + 1) % len(self.maps)

        # Indicateur de position
        info_font = pygame.font.SysFont(None, max(14, int(self.screen.get_width() * 0.02)))
        info_text = info_font.render(f"{self.current_index + 1} / {len(self.maps)}", True, config.COLOR_WHITE)
        ix = center_x - info_text.get_width() // 2
        iy = img_y + display_h + 12
        self.screen.blit(info_text, (ix, iy))

        return config.STATE_MAP_SELECT
