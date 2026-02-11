import pygame
from animsprite_pygame import Spritesheet, AnimatedSprite
import config

class Player:
    def __init__(self, x=0, y=0):
        """
        Initialise le joueur avec support de plusieurs animations.
        """
        self.max_health = 100
        self.health = self.max_health
        self.start_x = x
        self.start_y = y
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.ground_y = float(y)
        self.speed = 5
        self.velocity_y = 0.0
        self.on_ground = True
        self.jump_speed = config.PLAYER_JUMP_SPEED
        self.gravity = config.PLAYER_GRAVITY
        self.facing_dir = 1
        self.attack_range = config.PLAYER_ATTACK_RANGE
        self.attack_damage = config.PLAYER_ATTACK_DAMAGE
        self.attack_y_tolerance = config.PLAYER_ATTACK_Y_TOLERANCE
        self.kick_range = config.PLAYER_KICK_RANGE
        self.kick_damage = config.PLAYER_KICK_DAMAGE
        self.kick_y_tolerance = config.PLAYER_KICK_Y_TOLERANCE
        self.kick_knockback_distance = config.PLAYER_KICK_KNOCKBACK_DISTANCE
        self.kick_cooldown = config.PLAYER_KICK_COOLDOWN
        self.kick_miss_stun = config.PLAYER_KICK_MISS_STUN
        self.kick_cooldown_remaining = 0.0
        self.stun_remaining = 0.0
        self.attack_hit_done = False
        self.hits_taken_since_knockback = 0
        self.hits_for_knockback = config.HITS_FOR_KNOCKBACK
        self.knockback_distance = config.KNOCKBACK_DISTANCE
        self.knockback_speed = config.KNOCKBACK_SPEED
        self.knockback_remaining = 0.0
        self.knockback_dir = 0
        self.is_dead = False

        # Dictionnaire pour stocker les sprites par état
        self.sprites = {}  # {'idle': AnimatedSprite, 'walk_l': AnimatedSprite, 'walk_r': AnimatedSprite, ...}
        self.current_state = 'idle'
        self.current_action = 'idle'
        self.sprite = None

        # Variables de mouvement
        self.move_dir = 0
        self.velocity_x = 0

        # Lock pour animations non interruptibles (combo, attaque, etc.)
        self.locked = False
        self.attack_pressed = False
        self.kick_pressed = False
        self.jump_pressed = False

        # Charger les animations
        self._load_animations()
        self.attack_actions = [name for name in ("punch", "punch2") if name in self.sprites]
        self.next_attack_index = 0

    def _load_animations(self):
        self.load_animation("idle",   "assets/images/player/idle.png",   rows=8, animation_speed=0.12)
        self.load_animation("walk_l", "assets/images/player/walk_l.png", rows=8, animation_speed=0.15)
        self.load_animation("walk_r", "assets/images/player/walk_r.png", rows=8, animation_speed=0.15)
        self.load_animation("jump",   "assets/images/player/jump.png",   rows=5, animation_speed=0.2)
        self.load_animation("hit",    "assets/images/player/hit.png",    rows=4, animation_speed=0.09, loop=False)
        self.load_animation("death", "assets/images/player/death.png",   rows=10, animation_speed=0.1, loop=False)

        # Charger la spritesheet combo avec plusieurs sous-animations
        sheet_combo = Spritesheet("assets/images/player/combo.png")
        all_combo_frames = sheet_combo.get_sprites_from_grid(
            sprite_width=512,
            sprite_height=512,
            cols=1,
            rows=60
        )

        # Découper correctement les sous-animations
        combo_animations = {
            "punch": all_combo_frames[0:5],
            "punch2": all_combo_frames[13:18],
            "kick": all_combo_frames[6:11]
        }

        # Ajouter chaque combo dans self.sprites
        for name, frames in combo_animations.items():
            self.sprites[name] = AnimatedSprite(
                frames=frames,
                x=self.start_x,
                y=self.start_y,
                animation_speed=0.075,
                loop=False
            )

    def load_animation(self, state, spritesheet_path, sprite_width=512, sprite_height=512,
                       cols=1, rows=8, animation_speed=0.1, loop=True):
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
                loop=loop
            )

            if self.sprite is None or state == 'idle':
                self.sprite = self.sprites[state]

        except FileNotFoundError:
            print(f"Erreur: Le spritesheet '{spritesheet_path}' n'a pas été trouvé.")

    def handle_movement(self, keys):
        if self.is_dead:
            self.move_dir = 0
            self.velocity_x = 0
            self.attack_pressed = False
            self.kick_pressed = False
            self.jump_pressed = False
            return

        # Relacher les locks de touches quand les touches sont relees.
        if not keys[pygame.K_e]:
            self.attack_pressed = False
        if not keys[pygame.K_r]:
            self.kick_pressed = False
        if not keys[pygame.K_SPACE]:
            self.jump_pressed = False

        # Pendant le stun, on ne peut ni bouger ni attaquer.
        if self.stun_remaining > 0:
            self.move_dir = 0
            self.velocity_x = 0
            return

        if keys[pygame.K_SPACE] and not self.jump_pressed and self.on_ground and not self.locked:
            self.velocity_y = -self.jump_speed
            self.on_ground = False
            self.jump_pressed = True

        # Attaques
        if keys[pygame.K_e] and not self.attack_pressed and not self.locked:
            self.play_next_attack()
            self.attack_pressed = True

        if (
            keys[pygame.K_r]
            and not self.kick_pressed
            and not self.locked
            and self.kick_cooldown_remaining <= 0
        ):
            self.play_action("kick")
            self.kick_pressed = True
            self.kick_cooldown_remaining = self.kick_cooldown

        if self.locked:
            self.move_dir = 0
            self.velocity_x = 0
            return

        self.move_dir = 0
        self.velocity_x = 0

        if keys[pygame.K_q]:
            self.move_dir = -1
            self.facing_dir = -1
            self.velocity_x = -self.speed
        elif keys[pygame.K_d]:
            self.move_dir = 1
            self.facing_dir = 1
            self.velocity_x = self.speed

        self._update_action_from_movement()

    def _update_action_from_movement(self):
        if self.locked:
            return

        if not self.on_ground and "jump" in self.sprites:
            self.set_action("jump")
            return

        if self.move_dir == -1:
            self.set_action("walk_l")
        elif self.move_dir == 1:
            self.set_action("walk_r")
        else:
            self.set_action("idle")

    def set_action(self, action):
        """
        Définit l'action à effectuer si pas lockée.
        """
        if not self.locked and action in self.sprites:
            self.current_action = action

    def play_action(self, action):
        """
        Joue une animation non interruptible (combo, attaque, etc.).
        """
        if action in self.sprites:
            self.current_action = action
            self.locked = True
            if self._is_attack_action(action):
                self.attack_hit_done = False

            # Basculer directement sur le sprite d'action (one-shot)
            current_pos = (self.pos_x, self.pos_y)
            new_sprite = self.sprites[action]
            new_sprite.stop()
            new_sprite.reset()
            new_sprite.loop = self.sprites[action].loop
            new_sprite.rect.topleft = (int(current_pos[0]), int(current_pos[1]))
            self.sprite = new_sprite
            self.current_state = action
            self.sprite.play()

    def _is_attack_action(self, action):
        return action in self.attack_actions or action == "kick"

    def _get_attack_profile(self):
        """Retourne les parametres de hit selon l'attaque courante."""
        if self.current_action == "kick":
            return {
                "range": self.kick_range,
                "damage": self.kick_damage,
                "y_tolerance": self.kick_y_tolerance,
                "immediate_knockback": True,
                "knockback_distance": self.kick_knockback_distance
            }

        return {
            "range": self.attack_range,
            "damage": self.attack_damage,
            "y_tolerance": self.attack_y_tolerance,
            "immediate_knockback": False,
            "knockback_distance": None
        }

    def play_next_attack(self):
        if self.is_dead:
            return

        if not self.attack_actions:
            return

        action = self.attack_actions[self.next_attack_index]
        self.play_action(action)
        self.next_attack_index = (self.next_attack_index + 1) % len(self.attack_actions)

    def _start_knockback(self, source_dir, distance=None):
        """Declenche une poussee progressive dans la direction du coup."""
        if self.is_dead:
            return

        if source_dir == 0:
            return

        push_distance = self.knockback_distance if distance is None else max(0, distance)
        if push_distance <= 0:
            return

        self.knockback_dir = 1 if source_dir > 0 else -1
        self.knockback_remaining = float(push_distance)

    def die(self):
        """Passe le personnage en etat mort et joue l'animation de mort."""
        if self.is_dead:
            return

        self.is_dead = True
        self.health = 0
        self.move_dir = 0
        self.velocity_x = 0
        self.knockback_remaining = 0.0
        self.knockback_dir = 0
        self.attack_pressed = False
        self.kick_pressed = False
        self.jump_pressed = False
        self.kick_cooldown_remaining = 0.0
        self.stun_remaining = 0.0

        if "death" in self.sprites:
            self.play_action("death")
        else:
            self.locked = True

    def take_damage(self, amount, source_dir=0, immediate_knockback=False, knockback_distance=None):
        """Reduit les points de vie sans descendre sous 0."""
        if self.is_dead:
            return

        damage = max(0, amount)
        if damage <= 0 or self.health <= 0:
            return

        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.die()
            return

        if immediate_knockback:
            self._start_knockback(source_dir, distance=knockback_distance)
            self.hits_taken_since_knockback = 0
        else:
            self.hits_taken_since_knockback += 1
            if self.hits_taken_since_knockback >= self.hits_for_knockback:
                self._start_knockback(source_dir)
                self.hits_taken_since_knockback = 0

        if "hit" not in self.sprites:
            return

        # Evite de redemarrer l'animation hit en boucle pendant un meme impact.
        if self.locked and self.current_action == "hit":
            return

        self.play_action("hit")

    def try_hit_target(self, target):
        """
        Applique les degats si la cible est dans la portee du punch.
        Un punch ne peut toucher qu'une seule fois.
        """
        if self.is_dead:
            return False

        if not self.locked or not self._is_attack_action(self.current_action) or self.attack_hit_done:
            return False

        attack_profile = self._get_attack_profile()
        dx = target.pos_x - self.pos_x
        in_front = (
            0 <= dx <= attack_profile["range"]
            if self.facing_dir >= 0
            else -attack_profile["range"] <= dx <= 0
        )
        close_on_y = abs(target.pos_y - self.pos_y) <= attack_profile["y_tolerance"]

        if not in_front or not close_on_y:
            return False

        target.take_damage(
            attack_profile["damage"],
            source_dir=self.facing_dir,
            immediate_knockback=attack_profile["immediate_knockback"],
            knockback_distance=attack_profile["knockback_distance"]
        )
        self.attack_hit_done = True
        return True

    def _update_state(self):
        # Ne rien changer si locked et qu'on est dans la combo
        if self.locked and self.current_state == self.current_action:
            return

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
        if self.kick_cooldown_remaining > 0:
            self.kick_cooldown_remaining = max(0.0, self.kick_cooldown_remaining - delta_time)
        if self.stun_remaining > 0:
            self.stun_remaining = max(0.0, self.stun_remaining - delta_time)

        self._update_state()

        # Appliquer le mouvement horizontal + la poussee (knockback) progressive.
        knockback_velocity = 0.0
        delta_frames = delta_time * 60
        if self.knockback_remaining > 0 and self.knockback_dir != 0 and delta_frames > 0:
            frame_knockback = self.knockback_speed * delta_frames
            step = min(self.knockback_remaining, frame_knockback)
            knockback_velocity = self.knockback_dir * (step / delta_frames)
            self.knockback_remaining -= step

            if self.knockback_remaining <= 0:
                self.knockback_remaining = 0.0
                self.knockback_dir = 0

        self.pos_x += (self.velocity_x + knockback_velocity) * delta_frames

        if not self.on_ground:
            self.velocity_y += self.gravity * delta_frames
            self.pos_y += self.velocity_y * delta_frames
            if self.pos_y >= self.ground_y:
                self.pos_y = self.ground_y
                self.velocity_y = 0.0
                self.on_ground = True
        else:
            self.pos_y = self.ground_y

        if self.sprite:
            max_x = max(0, config.SCREEN_WIDTH - self.sprite.rect.width)
            clamped_x = max(0, min(max_x, self.pos_x))
            if clamped_x != self.pos_x:
                self.knockback_remaining = 0.0
                self.knockback_dir = 0
            self.pos_x = clamped_x

        self.sprite.rect.x = int(self.pos_x)
        self.sprite.rect.y = int(self.pos_y)

        # Mettre à jour le sprite
        self.sprite.update(delta_time)
        self.position = self.sprite.rect.topleft

        # Si animation non loop terminée -> revenir à idle
        if self.locked and not self.sprite.loop and self.sprite.is_finished:
            if self.is_dead and self.current_action == "death":
                self.sprite.stop()
                return

            if self.current_action == "kick" and not self.attack_hit_done:
                self.stun_remaining = max(self.stun_remaining, self.kick_miss_stun)

            self.locked = False
            self.set_action("idle")

    def draw(self, screen):
        if self.sprite:
            image = self.sprite.image
            if self.facing_dir < 0:
                image = pygame.transform.flip(image, True, False)

            screen.blit(image, self.sprite.rect)


    def set_position(self, x, y):
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.ground_y = float(y)
        self.velocity_y = 0.0
        self.on_ground = True
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
