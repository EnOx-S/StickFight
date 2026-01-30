import pygame
from animsprite_pygame import Spritesheet, AnimatedSprite
import config


class Player:
    def __init__(self, x=0, y=0):
        """
        Initialise le joueur avec support de plusieurs animations.
        """
        self.health = 100
        self.start_x = x
        self.start_y = y
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.speed = 5
        
        # Dictionnaire pour stocker les sprites par état
        self.sprites = {}  # {'idle': AnimatedSprite, 'walk_l': AnimatedSprite, 'walk_r': AnimatedSprite, ...}
        self.current_state = 'idle'
        self.current_action = 'idle'
        self.sprite = None
        
        # Variables de mouvement
        self.move_dir = 0
        self.velocity_x = 0
        
        # Charger les animations
        self._load_animations()
    
    def _load_animations(self):
        self.load_animation("idle",   "assets/images/player/idle.png",   rows=8, animation_speed=0.12)
        self.load_animation("walk_l", "assets/images/player/walk_l.png", rows=8, animation_speed=0.15)
        self.load_animation("walk_r", "assets/images/player/walk_r.png", rows=8, animation_speed=0.15)

    def load_animation(self, state, spritesheet_path, sprite_width=512, sprite_height=512, cols=1, rows=8, animation_speed=0.1):
        """
        Charge une animation pour un état donné.
        """
        try:
            sheet = Spritesheet(spritesheet_path)
            frames = sheet.get_sprites_from_grid(
                sprite_width=sprite_width,
                sprite_height=sprite_height,
                cols=cols,
                rows=rows
            )
            
            self.sprites[state] = AnimatedSprite(
                frames=frames,
                x=self.start_x,
                y=self.start_y,
                animation_speed=animation_speed,
                loop=True
            )
            
            if self.sprite is None or state == 'idle':
                self.sprite = self.sprites[state]
                
        except FileNotFoundError:
            print(f"Erreur: Le spritesheet '{spritesheet_path}' n'a pas été trouvé.")
    
    def handle_movement(self, keys):
        self.move_dir = 0
        self.velocity_x = 0

        if keys[pygame.K_q]:
            self.move_dir = -1
            self.velocity_x = -self.speed
        elif keys[pygame.K_d]:
            self.move_dir = 1
            self.velocity_x = self.speed

        self._update_action_from_movement()

    def _update_action_from_movement(self):
        if self.move_dir == -1:
            self.set_action("walk_l")
        elif self.move_dir == 1:
            self.set_action("walk_r")
        else:
            self.set_action("idle")

    def set_action(self, action):
        """
        Définit l'action à effectuer.
        """
        if action in self.sprites:
            self.current_action = action
    
    def _update_state(self):
        if self.current_action != self.current_state:
            current_pos = (self.pos_x, self.pos_y)
            if self.sprite:
                self.sprite.stop()
                self.sprite.reset()
            
            self.current_state = self.current_action
            new_sprite = self.sprites[self.current_state]
            
            # Conserver la position actuelle
            new_sprite.rect.topleft = (int(current_pos[0]), int(current_pos[1]))
            
            self.sprite = new_sprite
            self.sprite.play()
    
    def update(self, delta_time):
        self._update_state()
        
        # Appliquer le mouvement avec position float pour fluidité
        self.pos_x += self.velocity_x * delta_time * 60  # 60 pour compenser delta_time
        self.sprite.rect.x = int(self.pos_x)
        self.sprite.rect.y = int(self.pos_y)
        
        self.sprite.update(delta_time)
        self.position = self.sprite.rect.topleft
    
    def draw(self, screen):
        if self.sprite:
            screen.blit(self.sprite.image, self.sprite.rect)

    def set_position(self, x, y):
        self.pos_x = float(x)
        self.pos_y = float(y)
        for sprite in self.sprites.values():
            sprite.rect.topleft = (x, y)
        self.position = (x, y)
    
    def play_animation(self):
        if self.sprite:
            self.sprite.play()
    
    def stop_animation(self):
        if self.sprite:
            self.sprite.stop()
    
    def reset_animation(self):
        if self.sprite:
            self.sprite.reset()
