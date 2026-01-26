import os

import pygame
import button
from pygame._sdl2 import Image, Renderer, Texture, Window

# assets_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], "assets")

# pygame setup
pygame.init()
pygame.display.set_caption("StickFight")
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

# IMAGES LOADINGS

bgLoc = pygame.image.load("assets/images/background.png")
background = bgLoc.get_rect()

titleLoc = pygame.image.load("assets/images/title.png")
title = titleLoc.get_rect()

gameBgLoc = pygame.image.load("assets/images/game_background/soulsociety.png")
gameBgLoc = pygame.transform.scale(gameBgLoc, (screen.width, screen.height))
game_background = gameBgLoc.get_rect()

botBtnLoc = pygame.image.load("assets/images/bot.png")
# Centrer le bouton en soustrayant la moitié de sa taille
bot_btn_width = int(botBtnLoc.get_width() * 0.5)
bot_btn_height = int(botBtnLoc.get_height() * 0.5)
bot = button.Button(screen.width/2 - bot_btn_width/2, screen.height/2 - bot_btn_height/2, botBtnLoc, 0.5)

# Boutons settings et quitter (côte à côte)
settingsBtnLoc = pygame.image.load("assets/images/settings_button.png")
settings_btn_width = int(settingsBtnLoc.get_width() * 0.5)
settings_btn_height = int(settingsBtnLoc.get_height() * 0.5)
settings = button.Button(screen.width/2 - settings_btn_width - 20, screen.height/2 - bot_btn_height/2 + bot_btn_height + 80, settingsBtnLoc, 0.5)

quitBtnLoc = pygame.image.load("assets/images/close_button.png")
quit_btn_width = int(quitBtnLoc.get_width() * 0.5)
quit_btn_height = int(quitBtnLoc.get_height() * 0.5)
quit_btn = button.Button(screen.width/2 + 20, screen.height/2 - bot_btn_height/2 + bot_btn_height + 80, quitBtnLoc, 0.5)

# État de la fenêtre
current_screen = "menu"  # "menu" ou "game"

running = True

def draw_menu():
    screen.fill((0, 0, 0))  # Vider l'écran
    screen.blit(bgLoc, background)
    screen.blit(titleLoc, [screen.width/2-title.width/2, screen.height/5-title.height/5])

    if bot.draw(screen):
        return "game"
    
    if settings.draw(screen):
        print('SETTINGS')
    
    if quit_btn.draw(screen):
        return "quit"
    
    return "menu"

def draw_game(events):
    screen.fill((0, 0, 0))  # Vider l'écran
    screen.blit(gameBgLoc, game_background)  # Afficher le fond Soul Society
    #pygame.draw.text = pygame.font.Font(None, 36)
    #text = pygame.draw.text.render("GAME SCREEN", True, (255, 255, 255))
    #screen.blit(text, (screen.width/2 - text.get_width()/2, screen.height/2))
    
    # Appuyer sur ESC pour revenir au menu
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
    
    return "game"

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if current_screen == "menu":
        current_screen = draw_menu()
        if current_screen == "quit":
            running = False
    elif current_screen == "game":
        current_screen = draw_game(events)
    
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()