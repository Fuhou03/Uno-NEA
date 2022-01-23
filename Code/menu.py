import pygame
from button import Button
from login import SignIn

class Menu:
    def __init__(self, interface):
        self.interface = interface
        self.run_display = True

        self.MID_W, self.MID_H = 390, 350

        self.button_font = pygame.font.Font(None, 90)
        self.text_font = pygame.font.Font(None, 30)

    def reset_keys(self):
        self.interface.ENTER_KEY = False
        self.interface.BACK_KEY = False
        self.interface.DOWN_KEY = False
        self.interface.UP_KEY = False

class MainMenu(Menu):
    def __init__(self, interface):
        super().__init__(interface)

        self.play_label = self.button_font.render("Play", True, (255, 255, 255))
        self.option_label = self.button_font.render("Options", True, (255, 255, 255))
        self.enter_desc = self.text_font.render("Press Enter To Select", True, (255, 255, 255))
        self.back_desc = self.text_font.render("Press Backspace To Go Back", True, (255, 255, 255))

        self.PLAY_X, self.PLAY_Y = self.MID_W, self.MID_H - 70
        self.play_button = Button(self.PLAY_X, self.PLAY_Y, 280, 85)

        self.OPTION_X, self.OPTION_Y = self.MID_W, self.MID_H + 70
        self.option_button = Button(self.OPTION_X, self.OPTION_Y, 280, 85)

        self.cursor = Button(self.PLAY_X, self.PLAY_Y, 280, 85)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.play_button, self.option_button, self.cursor]

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.play_label, (self.MID_W + 62, self.MID_H - 60))
            self.interface.screen.blit(self.option_label, (self.MID_W + 17, self.MID_H + 82))

            self.interface.screen.blit(self.enter_desc, (self.MID_W + 310, self.MID_H + 400))
            self.interface.screen.blit(self.back_desc, (self.MID_W - 350, self.MID_H + 400))

            self.interface.check_events()
            self.check_input()

            for b in self.button_list:
                b.draw_rect(self.interface.screen)

            pygame.display.update()
            self.interface.clock.tick(60)   # 60 fps
            self.reset_keys()

    def move_cursor(self):
        if self.cursor.rect.y != self.option_button.rect.y:     # Stops the cursor from moving away from buttons
            if self.interface.DOWN_KEY:     # To select a button
                self.cursor.rect.y += 140
        elif self.cursor.rect.y != self.play_button.rect.y:
            if self.interface.UP_KEY:
                self.cursor.rect.y -= 140

    def check_input(self):
        self.move_cursor()

        if self.interface.ENTER_KEY:    # If they pressed enter
            for button in self.button_list:     # Finds the button selected
                if button.rect.y == self.cursor.rect.y:     # If the cursor rect overlaps with that button
                    if button == self.play_button:
                        # Move onto game_mode screen
                        print("Play")

                    elif button == self.option_button:
                        self.interface.current_screen = self.interface.options
                        self.run_display = False






class Options(Menu):
    def __init__(self, interface):
        super().__init__(interface)
        self.font = pygame.font.Font(None, 50)

        self.volume_label = self.font.render("Volume", True, (255, 255, 255))
        self.volume_button = Button(self.MID_W - 180, self.MID_H + 100, 190, 50)

        self.music_label = self.font.render("Music", True, (255, 255, 255))
        self.music_button = Button(self.MID_W - 180, self.MID_H, 190, 50)

        self.sound_label = self.font.render("Sound", True, (255, 255, 255))
        self.sound_button = Button(self.MID_W - 180, self.MID_H - 100, 190, 50)

        self.button_list = [self.volume_button, self.music_button, self.sound_button]


    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.volume_label, (self.MID_W - 146, self.MID_H - 93))
            self.interface.screen.blit(self.music_label, (self.MID_W - 136, self.MID_H + 7))
            self.interface.screen.blit(self.sound_label, (self.MID_W - 141, self.MID_H + 107))

            self.interface.check_events()
            self.check_input()
            for b in self.button_list:
                b.draw_rect(self.interface.screen)
            pygame.display.update()
            self.interface.clock.tick(60)   # 60 fps
            self.reset_keys()



    def check_input(self):   # Create sliders or options later
        if self.interface.BACK_KEY:
                self.interface.current_screen = self.interface.main_menu
                self.run_display = False


class GameMode(Menu):
    def __init__(self, interface):
        super().__init__(interface)




