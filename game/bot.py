import pygame
from animsprite_pygame import Spritesheet, AnimatedSprite
import config
from game.player import Player

class Bot(Player):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.current_state = 'idle'
        for anim in self.sprites.values():
            anim.frames = [
                pygame.transform.flip(frame, True, False)
                for frame in anim.frames
            ]
    def handle_movement(self, keys):
        pass