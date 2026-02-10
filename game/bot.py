import random
import pygame
from game.player import Player


class Bot(Player):
    def __init__(self, x=0, y=0, target=None):
        super().__init__(x, y)

        self.target = target

        # IA tuning
        self.attack_probability = 0.8
        self.kick_probability = 0.2
        self.too_close_distance = 40
        self.far_distance = self.attack_range + 20

        # Humanisation
        self.decision_delay_min = 0.15
        self.decision_delay_max = 0.35
        self.decision_timer = 0.0

        # État courant
        self.current_ai_state = "idle"

        # Flip sprites (bot regarde par défaut à gauche)
        self.facing_dir = -1
        for anim in self.sprites.values():
            anim.frames = [
                pygame.transform.flip(frame, True, False)
                for frame in anim.frames
            ]

    def handle_movement(self, _keys=None):
        if not self.target or self.is_dead:
            self.move_dir = 0
            self.velocity_x = 0
            return

        # Stun / lock → aucune décision ni mouvement
        if self.stun_remaining > 0 or self.locked:
            self.move_dir = 0
            self.velocity_x = 0
            return

        dx = self.target.pos_x - self.pos_x
        abs_dx = abs(dx)
        dy = abs(self.target.pos_y - self.pos_y)

        # Orientation
        self.facing_dir = 1 if dx > 0 else -1

        in_attack_range = (
            abs_dx <= self.attack_range
            and dy <= self.attack_y_tolerance
        )

        in_kick_range = (
            abs_dx <= self.kick_range
            and dy <= self.kick_y_tolerance
        )

        # Nouvelle décision seulement si timer écoulé
        if self.decision_timer <= 0:
            self.current_ai_state = self._choose_state(abs_dx, in_attack_range, in_kick_range)
            self.decision_timer = random.uniform(
                self.decision_delay_min,
                self.decision_delay_max
            )

        # Toujours décrémenter le timer
        self.decision_timer = max(0.0, self.decision_timer - 1/60)  # delta approximation

        # Exécution de l'état courant
        if self.current_ai_state == "approach":
            self._approach()
        elif self.current_ai_state == "reposition":
            self._reposition()
        elif self.current_ai_state == "attack":
            self.play_next_attack()
        elif self.current_ai_state == "kick":
            if self.kick_cooldown_remaining <= 0:
                self.play_action("kick")
                self.kick_cooldown_remaining = self.kick_cooldown
        else:  # idle
            self.move_dir = 0
            self.velocity_x = 0
            self.set_action("idle")

    def _choose_state(self, abs_dx, in_attack_range, in_kick_range):
        if abs_dx > self.far_distance:
            return "approach"
        if abs_dx < self.too_close_distance:
            return "reposition"
        if in_attack_range and random.random() < self.attack_probability:
            return "attack"
        if in_kick_range and self.kick_cooldown_remaining <= 0 and random.random() < self.kick_probability:
            return "kick"
        return "idle"

    def _approach(self):
        self.move_dir = self.facing_dir
        self.velocity_x = self.speed * self.facing_dir   # signe correct
        self._update_action_from_movement()

    def _reposition(self):
        self.move_dir = -self.facing_dir
        self.velocity_x = self.speed * -self.facing_dir  # signe correct
        self._update_action_from_movement()


    def update(self, delta_time):
        # Décrément réel du timer
        self.decision_timer = max(0.0, self.decision_timer - delta_time)

        # Appel de Player.update() pour mouvement, gravité et animations
        super().update(delta_time)
