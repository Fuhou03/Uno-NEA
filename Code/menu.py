import pygame
from button import Button

class Menu:
    def __init__(self, interface):
        self.interface = interface
        self.run_display = True

        self.MID_W, self.MID_H = 390, 350

        self.menu_font = pygame.font.Font(None, 90)
        self.text_font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 50)

        self.enter_desc = self.text_font.render("Enter To Select", True, (255, 255, 255))
        self.back_desc = self.text_font.render("Backspace To Return", True, (255, 255, 255))
        self.arrow_desc = self.text_font.render("Arrows To Navigate", True, (255, 255, 255))

    def reset_keys(self):
        self.interface.ENTER_KEY = False
        self.interface.BACK_KEY = False
        self.interface.DOWN_KEY = False
        self.interface.UP_KEY = False

class MainMenu(Menu):
    def __init__(self, interface):
        super().__init__(interface)
        self.title_font = pygame.font.Font(None, 170)
        self.play_label = self.menu_font.render("Play", True, (255, 255, 255))
        self.option_label = self.menu_font.render("Options", True, (255, 255, 255))

        self.title = self.title_font.render("Uno", True, (255, 255, 255))

        self.PLAY_X, self.PLAY_Y = self.MID_W, self.MID_H - 70
        self.play_button = Button(self.PLAY_X, self.PLAY_Y, 280, 90)    # x, y, width, height

        self.OPTION_X, self.OPTION_Y = self.MID_W, self.MID_H + 70
        self.option_button = Button(self.OPTION_X, self.OPTION_Y, 280, 90)

        self.cursor = Button(self.PLAY_X, self.PLAY_Y, 280, 90)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.play_button, self.option_button, self.cursor]

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.title, (self.MID_W + 15, self.MID_H - 280))
            self.interface.screen.blit(self.play_label, (self.MID_W + 70, self.MID_H - 55))
            self.interface.screen.blit(self.option_label, (self.MID_W + 17, self.MID_H + 82))

            self.interface.screen.blit(self.enter_desc, (self.MID_W + 390, self.MID_H + 400))
            self.interface.screen.blit(self.back_desc, (self.MID_W - 330, self.MID_H + 400))
            self.interface.screen.blit(self.arrow_desc, (self.MID_W + 40, self.MID_H + 400))

            self.interface.check_events()
            self.check_input()

            for b in self.button_list:
                b.draw_rect(self.interface.screen)

            pygame.display.update()
            self.interface.clock.tick(60)   # 60 fps
            self.reset_keys()

    def move_cursor(self):
        if self.interface.DOWN_KEY:     # If they pressed the Down arrow key
            if self.cursor.rect.y != self.option_button.rect.y:     # Stops the cursor from moving above/below button
                self.cursor.rect.y += 140   # Moves the cursor up and down

        if self.interface.UP_KEY:
            if self.cursor.rect.y != self.play_button.rect.y:
                self.cursor.rect.y -= 140

    def check_input(self):
        self.move_cursor()

        if self.interface.ENTER_KEY:    # If they pressed enter
            for button in self.button_list:     # Finds the button selected
                if button.rect.y == self.cursor.rect.y:     # If the cursor rect overlaps with that button
                    if button == self.play_button:
                        self.interface.current_screen = self.interface.game_mode    # Changes to game mode menu
                        self.run_display = False

                    elif button == self.option_button:
                        self.interface.current_screen = self.interface.options
                        self.run_display = False


class Options(Menu):
    def __init__(self, interface):
        super().__init__(interface)
        self.font = pygame.font.Font(None, 50)

        self.volume_label = self.button_font.render("Volume", True, (255, 255, 255))
        self.volume_button = Button(self.MID_W - 180, self.MID_H + 100, 190, 50)

        self.music_label = self.button_font.render("Music", True, (255, 255, 255))
        self.music_button = Button(self.MID_W - 180, self.MID_H, 190, 50)

        self.sound_label = self.button_font.render("Sound", True, (255, 255, 255))
        self.sound_button = Button(self.MID_W - 180, self.MID_H - 100, 190, 50)

        self.button_list = [self.volume_button, self.music_button, self.sound_button]


    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.volume_label, (self.MID_W - 146, self.MID_H - 93))
            self.interface.screen.blit(self.music_label, (self.MID_W - 136, self.MID_H + 7))
            self.interface.screen.blit(self.sound_label, (self.MID_W - 141, self.MID_H + 107))

            self.interface.screen.blit(self.enter_desc, (self.MID_W + 390, self.MID_H + 400))
            self.interface.screen.blit(self.back_desc, (self.MID_W - 330, self.MID_H + 400))
            self.interface.screen.blit(self.arrow_desc, (self.MID_W + 40, self.MID_H + 400))

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
        self.font = pygame.font.Font(None, 50)

        self.two_player_label = self.button_font.render("Two Player", True, (255, 255, 255))
        self.two_player_button = Button(self.MID_W, self.MID_H - 120, 280, 60)  # x, y, width, height

        self.three_player_label = self.button_font.render("Three Player", True, (255, 255, 255))
        self.three_player_button = Button(self.MID_W, self.MID_H, 280, 60)

        self.four_player_label = self.button_font.render("Four Player", True, (255, 255, 255))
        self.four_player_button = Button(self.MID_W, self.MID_H + 120, 280, 60)

        self.cursor = Button(self.MID_W, self.MID_H - 120, 280, 60)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.two_player_button, self.three_player_button, self.four_player_button, self.cursor]

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.two_player_label, (self.MID_W + 42, self.MID_H - 105))
            self.interface.screen.blit(self.three_player_label, (self.MID_W + 32, self.MID_H + 15))
            self.interface.screen.blit(self.four_player_label, (self.MID_W + 40, self.MID_H + 133))

            self.interface.screen.blit(self.enter_desc, (self.MID_W + 390, self.MID_H + 400))
            self.interface.screen.blit(self.back_desc, (self.MID_W - 330, self.MID_H + 400))
            self.interface.screen.blit(self.arrow_desc, (self.MID_W + 40, self.MID_H + 400))

            self.interface.check_events()
            self.check_input()

            for b in self.button_list:
                b.draw_rect(self.interface.screen)

            pygame.display.update()
            self.interface.clock.tick(60)   # 60 fps
            self.reset_keys()

    def move_cursor(self):
        if self.interface.DOWN_KEY:
            if self.cursor.rect.y != self.four_player_button.rect.y:     # Stops the cursor from moving away from buttons
                self.cursor.rect.y += 120

        if self.interface.UP_KEY:
            if self.cursor.rect.y != self.two_player_button.rect.y:
                self.cursor.rect.y -= 120


    def check_input(self):
        self.move_cursor()

        if self.interface.ENTER_KEY:    # If they pressed enter
            for button in self.button_list:     # Finds the button selected
                if button.rect.y == self.cursor.rect.y:     # If the cursor rect overlaps with that button

                    if button == self.two_player_button:
                        self.interface.game_mode_choice = 2
                        self.run_display = False
                        self.interface.running = False    # Stops the display

                    elif button == self.three_player_button:
                        self.interface.game_mode_choice = 3
                        self.run_display = False
                        self.interface.running = False    # Stops the display

                    elif button == self.four_player_button:
                        self.interface.game_mode_choice = 4
                        self.run_display = False
                        self.interface.running = False    # Stops the display


        elif self.interface.BACK_KEY:   # Goes back to the main menu
            self.interface.current_screen = self.interface.main_menu
            self.run_display = False




