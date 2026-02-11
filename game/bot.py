import random
import pygame
from game.player import Player


class Bot(Player):
    def __init__(self, x=0, y=0, target=None):
        super().__init__(x, y)

        self.target = target

        # =============================
        # IA BASE
        # =============================
        self.too_close_distance = 40
        self.far_distance = self.attack_range + 30

        self.decision_delay_min = 0.15
        self.decision_delay_max = 0.35
        self.decision_timer = 0.0

        self.attack_global_cooldown = 0.5
        self.attack_cooldown_remaining = 0.0

        self.current_ai_state = "idle"

        # =============================
        # IA ADAPTATIVE
        # =============================
        self.style = "balanced"
        self.tempo_multiplier = 1.0

        self.analysis_timer = 0.0
        self.analysis_window = 4.0

        self.player_recent_attacks = 0
        self.player_jump_counter = 0
        self.player_air_attack_counter = 0

        self.spam_threshold = 4

        # =============================
        # HUMANISATION
        # =============================
        self.error_chance = 0.05

        # =============================
        # SAUT
        # =============================
        self.jump_probability = 0.25
        self.air_attack_probability = 0.5

        # Regarde à gauche par défaut
        self.facing_dir = -1
        #for anim in self.sprites.values():
        #    anim.frames = [
        #        pygame.transform.flip(frame, True, False)
        #        for frame in anim.frames
        #    ]

    # ======================================================
    # OBSERVATION JOUEUR
    # ======================================================

    def observe_player(self):
        if not self.target:
            return

        # Compte attaques
        if (
            self.target.locked
            and self.target._is_attack_action(self.target.current_action)
        ):
            self.player_recent_attacks += 1

            # Attaque aérienne
            if not self.target.on_ground:
                self.player_air_attack_counter += 1

        # Compte sauts
        if not self.target.on_ground:
            self.player_jump_counter += 1

    # ======================================================
    # ADAPTATION STYLE
    # ======================================================

    def _adapt_style(self):
        if not self.target:
            return

        health_ratio = self.health / self.max_health
        health_diff = self.health - self.target.health

        # Anti spam air
        if self.player_jump_counter > 5:
            self.style = "anti_air"

        elif self.player_recent_attacks >= self.spam_threshold:
            self.style = "punisher"

        elif health_ratio < 0.3:
            self.style = "aggressive"

        elif health_diff > 20:
            self.style = "aggressive"

        else:
            self.style = "balanced"

        # Tempo
        if self.style == "aggressive":
            self.tempo_multiplier = 0.75
        elif self.style == "anti_air":
            self.tempo_multiplier = 0.85
        elif self.style == "punisher":
            self.tempo_multiplier = 0.85
        else:
            self.tempo_multiplier = 1.0

    # ======================================================
    # CHOIX ÉTAT IA
    # ======================================================

    def _choose_state(self, abs_dx, in_attack_range, in_kick_range):

        if random.random() < self.error_chance:
            return random.choice(["idle", "reposition"])

        if self.style == "aggressive":
            attack_prob = 0.75
            kick_prob = 0.3

        elif self.style == "punisher":
            attack_prob = 0.8
            kick_prob = 0.35

        elif self.style == "anti_air":
            attack_prob = 0.7
            kick_prob = 0.2

        else:
            attack_prob = 0.6
            kick_prob = 0.2

        # ===== ANTI AIR PRIORITAIRE =====
        if (
            self.style == "anti_air"
            and not self.target.on_ground
            and abs_dx <= self.attack_range + 20
            and self.attack_cooldown_remaining <= 0
        ):
            return "attack"

        # Décision saut
        if (
            self.on_ground
            and random.random() < self.jump_probability
            and abs_dx < self.attack_range + 60
        ):
            return "jump"

        if abs_dx > self.far_distance:
            return "approach"

        if abs_dx < self.too_close_distance:
            if random.random() < 0.6:
                return "attack"
            return "reposition"

        if (
            in_attack_range
            and self.attack_cooldown_remaining <= 0
            and random.random() < attack_prob
        ):
            return "attack"

        if (
            in_kick_range
            and self.kick_cooldown_remaining <= 0
            and random.random() < kick_prob
        ):
            return "kick"

        return "idle"

    # ======================================================
    # HANDLE MOVEMENT
    # ======================================================

    def handle_movement(self, _keys=None):
        if not self.target or self.is_dead:
            self.move_dir = 0
            self.velocity_x = 0
            return

        if self.stun_remaining > 0 or self.locked:
            self.move_dir = 0
            self.velocity_x = 0
            return

        dx = self.target.pos_x - self.pos_x
        abs_dx = abs(dx)
        dy = abs(self.target.pos_y - self.pos_y)

        self.facing_dir = 1 if dx > 0 else -1

        in_attack_range = (
            abs_dx <= self.attack_range
            and dy <= self.attack_y_tolerance
        )

        in_kick_range = (
            abs_dx <= self.kick_range
            and dy <= self.kick_y_tolerance
        )

        # Recul intelligent si joueur saute vers lui
        if (
            not self.target.on_ground
            and abs_dx < self.attack_range
        ):
            self.move_dir = -self.facing_dir
            self.velocity_x = self.speed * -self.facing_dir

        if self.decision_timer <= 0:
            self.current_ai_state = self._choose_state(
                abs_dx,
                in_attack_range,
                in_kick_range
            )

            self.decision_timer = random.uniform(
                self.decision_delay_min,
                self.decision_delay_max
            ) * self.tempo_multiplier

        # ===== EXÉCUTION =====

        if self.current_ai_state == "approach":
            self.move_dir = self.facing_dir
            self.velocity_x = self.speed * self.facing_dir

        elif self.current_ai_state == "reposition":
            self.move_dir = -self.facing_dir
            self.velocity_x = self.speed * -self.facing_dir

        elif self.current_ai_state == "jump":
            if self.on_ground:
                self.velocity_y = -self.jump_speed
                self.on_ground = False
                self.move_dir = self.facing_dir
                self.velocity_x = self.speed * 0.6 * self.facing_dir
                self.set_action("jump")

        elif self.current_ai_state == "attack":
            if self.attack_cooldown_remaining <= 0:
                self.play_next_attack()
                self.attack_cooldown_remaining = self.attack_global_cooldown

        elif self.current_ai_state == "kick":
            if self.kick_cooldown_remaining <= 0:
                self.play_action("kick")
                self.kick_cooldown_remaining = self.kick_cooldown

        else:
            self.move_dir = 0
            self.velocity_x = 0

        # Animation saut automatique
        if not self.on_ground:
            self.set_action("jump")
        else:
            self._update_action_from_movement()

        # Attaque aérienne
        if (
            not self.on_ground
            and in_attack_range
            and self.attack_cooldown_remaining <= 0
            and random.random() < self.air_attack_probability
        ):
            self.play_next_attack()
            self.attack_cooldown_remaining = self.attack_global_cooldown

    # ======================================================
    # UPDATE
    # ======================================================

    def update(self, delta_time):

        self.decision_timer = max(0.0, self.decision_timer - delta_time)
        self.attack_cooldown_remaining = max(
            0.0,
            self.attack_cooldown_remaining - delta_time
        )

        self.analysis_timer += delta_time
        self.observe_player()

        if self.analysis_timer >= self.analysis_window:
            self._adapt_style()
            self.analysis_timer = 0.0
            self.player_recent_attacks = 0
            self.player_jump_counter = 0
            self.player_air_attack_counter = 0

        super().update(delta_time)
