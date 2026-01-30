"""
Gestion des boutons interactifs.
Classe Button pour créer des boutons clickables avec détection de souris.
"""

import pygame


class Button:
    """
    Représente un bouton clickable dans le jeu.
    
    Attributs:
        x, y: Position du bouton
        image: Image du bouton
        scale: Échelle de redimensionnement (0.5 = 50% de la taille d'origine)
    """
    
    def __init__(self, x, y, image, scale):
        """
        Initialise le bouton.
        
        Args:
            x (int): Position x du bouton
            y (int): Position y du bouton
            image (pygame.Surface): Image du bouton
            scale (float): Échelle de redimensionnement
        """
        width = image.get_width()
        height = image.get_height()

        # Redimensionner l'image
        self.image = pygame.transform.scale(
            image,
            (int(width * scale), int(height * scale))
        )

        # Créer un rectangle pour la collision
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """
        Affiche le bouton et détecte si l'utilisateur a cliqué dessus.
        
        Args:
            surface (pygame.Surface): La surface où afficher le bouton
            
        Returns:
            bool: True si le bouton a été cliqué, False sinon
        """
        action = False

        # Obtenir la position de la souris
        pos = pygame.mouse.get_pos()

        # Vérifier si la souris est sur le bouton et s'il y a un clic
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        # Réinitialiser le clic quand la souris est relâchée
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        # Afficher le bouton
        surface.blit(self.image, self.rect)

        return action
