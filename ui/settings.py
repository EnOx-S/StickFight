import pygame
import config
import sys
from asyncio import events
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from ui.button import Button

class SettingsScreen:
    def __init__(self,screen):
        self.screen = screen
        self._load_assets()
        self.zoom_factor = 1.0  
        self.target_zoom = 1.25  
        self.zoom_speed = 0.02  
        self.current_tab = "audio"
        
        self.slider = Slider(self.screen, 750, 300, 500, 40, min=0, max=100, step=1)
        self.output = TextBox(self.screen, 1040, 350, 70, 40, fontSize=25)
        self.slider2 = Slider(self.screen, 750, 400, 500, 40, min=0, max=100, step=1)
        self.output2 = TextBox(self.screen, 1040, 450, 70, 40, fontSize=25)
        self.slider3 = Slider(self.screen, 750, 500, 500, 40, min=0, max=100, step=1)
        self.output3 = TextBox(self.screen, 1040, 550, 70, 40, fontSize=25)
        
        self.output.disable()
        self.output2.disable()
        self.output3.disable()
        # Pour rebinding des touches
        self.awaiting_bind = None

    def _load_assets(self):
        background_image = pygame.image.load(config.SETTINGS_PATH)
        self.background_image = pygame.transform.scale(
            background_image,
            (self.screen.get_width(), self.screen.get_height())
        )
        self.background_rect = self.background_image.get_rect()

        controles_btn_image = pygame.image.load(config.CONTROLES_BTN_PATH)
        audio_btn_image = pygame.image.load(config.AUDIO_BTN_PATH)

        credit_btn_image = pygame.image.load(config.CREDIT_BTN_PATH)
        quit_btn_image = pygame.image.load("assets/images/main_screen/quit.png")

        controles_width = int(controles_btn_image.get_width())
        controles_height = int(controles_btn_image.get_height())
        audio_width = int(audio_btn_image.get_width())
        audio_height = int(audio_btn_image.get_height())
        credit_width = int(credit_btn_image.get_width())
        credit_height = int(credit_btn_image.get_height())
        quit_width = int(quit_btn_image.get_width() * config.BUTTON_SCALE)
        quit_height = int(quit_btn_image.get_height() * config.BUTTON_SCALE)

        screen_width = self.screen.get_width()
        top_y = 80 
        total_width = controles_width + audio_width + credit_width + 2 * config.BUTTON_SPACING
        start_x = (screen_width - total_width) / 2

        self.controles_button = Button(
            start_x,
            top_y,
            controles_btn_image,
            config.BIG_BUTTON_SCALE
        )
        self.audio_button = Button(
            start_x + controles_width + config.BUTTON_SPACING,
            top_y,
            audio_btn_image,
            config.BIG_BUTTON_SCALE
        )
        self.credit_button = Button(
            start_x + controles_width + config.BUTTON_SPACING + audio_width + config.BUTTON_SPACING,
            top_y,
            credit_btn_image,
            config.BIG_BUTTON_SCALE
        )

        quit_x = (self.screen.get_width() - quit_width) / 2
        quit_y = self.screen.get_height() - quit_height - 60
        self.quit_button = Button(
            quit_x,
            quit_y,
            quit_btn_image,
            config.BUTTON_SCALE
        )

    def draw(self, events):
        self.screen.fill(config.COLOR_BLACK)

        if self.zoom_factor < self.target_zoom:
            self.zoom_factor += self.zoom_speed
            if self.zoom_factor > self.target_zoom:
                self.zoom_factor = self.target_zoom

        zoom_w = int(self.screen.get_width() * self.zoom_factor)
        zoom_h = int(self.screen.get_height() * self.zoom_factor)
        zoomed_bg = pygame.transform.smoothscale(self.background_image, (zoom_w, zoom_h))
        bg_x = (self.screen.get_width() - zoom_w) // 2
        bg_y = (self.screen.get_height() - zoom_h) // 2 + 80
        self.screen.blit(zoomed_bg, (bg_x, bg_y))

        if self.current_tab == "audio":
            pygame_widgets.update(events)
            
            self.output.setText(str(self.slider.getValue()))
            self.output2.setText(str(self.slider2.getValue()))
            self.output3.setText(str(self.slider3.getValue()))

            font = pygame.font.Font(None, 40)
            label1 = font.render("Main Audio", True, (255, 255, 255))
            self.screen.blit(label1, (500, 310))
            
            label2 = font.render("Music", True, (255, 255, 255))
            self.screen.blit(label2, (500, 410))
            
            label3 = font.render("SFX", True, (255, 255, 255))
            self.screen.blit(label3, (500, 510))

        if self.controles_button.draw(self.screen):
            self.current_tab = "controles"

        if self.current_tab == "controles":
            font = pygame.font.Font(None, 40)
            actions = [
                ("left", "Gauche"),
                ("right", "Droite"),
                ("jump", "Saut"),
                ("attack", "Coup de poing"),
                ("kick", "Coup de pied"),
            ]

            start_x = 500
            start_y = 300
            spacing_y = 70
            btn_w = 300
            btn_h = 50

            rects = {}
            for i, (key, label) in enumerate(actions):
                y = start_y + i * spacing_y
                label_surf = font.render(label, True, (255, 255, 255))
                self.screen.blit(label_surf, (start_x, y))

                btn_rect = pygame.Rect(start_x + 250, y, btn_w, btn_h)
                pygame.draw.rect(self.screen, (60, 60, 60), btn_rect)

                # use key name from config
                key_name = pygame.key.name(config.KEY_BINDINGS.get(key, pygame.K_UNKNOWN))
                key_surf = font.render(key_name, True, (255, 255, 255))
                self.screen.blit(key_surf, (btn_rect.x + 10, btn_rect.y + 8))

                if self.awaiting_bind == key:
                    pygame.draw.rect(self.screen, (200, 50, 50), btn_rect, 3)

                rects[key] = btn_rect

            if self.awaiting_bind:
                info = font.render("Appuyez sur une touche pour lier...", True, (255, 200, 200))
                self.screen.blit(info, (start_x, start_y - 60))

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for k, r in rects.items():
                        if r.collidepoint(event.pos):
                            self.awaiting_bind = k
                if event.type == pygame.KEYDOWN and self.awaiting_bind:
                    # assign and stop waiting
                    config.KEY_BINDINGS[self.awaiting_bind] = event.key
                    self.awaiting_bind = None

        if self.audio_button.draw(self.screen):
            self.current_tab = "audio"

        if self.credit_button.draw(self.screen):
            self.current_tab = "credit"
        
        if self.current_tab == "credit":
            font_title = pygame.font.Font(None, 60)
            title = font_title.render("Fait par : Enzo , Marwan , Mounir and Ylian", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
            self.screen.blit(title, title_rect)
            
            font_inspired = pygame.font.Font(None, 70)
            inspired = font_inspired.render("Inspiré de Mortal Kombat", True, (255, 255, 255))
            inspired_rect = inspired.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 250))
            self.screen.blit(inspired, inspired_rect)

        if self.quit_button.draw(self.screen):
            return config.STATE_MENU

        return config.STATE_SETTINGS