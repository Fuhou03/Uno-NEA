import pygame
from button import Button
import webbrowser


class Menu:
    def __init__(self, interface):
        self.interface = interface
        self.run_display = True

        self.MID_W, self.MID_H = (self.interface.SCREEN_W / 2), (self.interface.SCREEN_H / 2)

        self.text_font = pygame.font.Font(None, 40)
        self.button_font = pygame.font.Font(None, 60)

        self.enter_desc = self.text_font.render("Enter To Select", True, (255, 255, 255))
        self.back_desc = self.text_font.render("Backspace To Return", True, (255, 255, 255))
        self.arrow_desc = self.text_font.render("Arrows To Navigate", True, (255, 255, 255))

        self.menu_sound = pygame.mixer.Sound("Sounds\menu sound.wav")
        self.menu_sound.set_volume(self.interface.volume)

    def reset_keys(self):       # Every menu can use this method
        self.interface.ENTER_KEY = False
        self.interface.BACK_KEY = False
        self.interface.DOWN_KEY = False
        self.interface.UP_KEY = False
        self.interface.RIGHT_KEY = False
        self.interface.LEFT_KEY = False

    def blit_description(self):
        self.interface.screen.blit(self.enter_desc, (self.MID_W + 300, self.MID_H + 400))
        self.interface.screen.blit(self.back_desc, (self.MID_W - 520, self.MID_H + 400))
        self.interface.screen.blit(self.arrow_desc, (self.MID_W - self.arrow_desc.get_width() / 2, self.MID_H + 400))


class MainMenu(Menu):
    def __init__(self, interface):      # Having interface as an argument allows us to its variables and the screen
        super().__init__(interface)     # Inherit from Menu class to access its attributes and methods
        self.menu_font = pygame.font.Font(None, 100)
        self.title_font = pygame.font.Font(None, 170)
        self.play_label = self.menu_font.render("Play", True, (255, 255, 255))
        self.option_label = self.menu_font.render("Options", True, (255, 255, 255))
        self.rules_label = self.menu_font.render("Rules", True, (255, 255, 255))

        self.title = self.title_font.render("Uno", True, (255, 255, 255))

        # x, y for top left corner of the rectangle and then width, height
        self.play_button = Button(self.MID_W - 160, self.MID_H - 130, 320, 100)
        self.option_button = Button(self.MID_W - 160, self.MID_H + 30, 320, 100)
        self.rules_button = Button(self.MID_W - 160, self.MID_H + 190, 320, 100)

        self.cursor = Button(self.MID_W - 160, self.MID_H - 130, 320, 100)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.play_button, self.option_button, self.rules_button, self.cursor]

    def display(self):
        """ Displays the text and buttons and checks if they pressed a key """
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.menu_sound.set_volume(self.interface.volume)

            self.interface.screen.blit(self.title, (self.MID_W - self.title.get_width() / 2,    # This centres the text
                                       self.MID_H - 320))
            self.interface.screen.blit(self.play_label, (self.MID_W - self.play_label.get_width() / 2,
                                        self.MID_H - 110))
            self.interface.screen.blit(self.option_label, (self.MID_W - self.option_label.get_width() / 2,
                                       self.MID_H + 50))
            self.interface.screen.blit(self.rules_label, (self.MID_W - self.rules_label.get_width() / 2,
                                                           self.MID_H + 210))

            self.blit_description()

            self.interface.check_events()
            self.check_input()

            for b in self.button_list:
                b.draw_rect(self.interface.screen)

            pygame.display.update()
            self.interface.clock.tick(60)   # 60 fps
            self.reset_keys()

    def move_cursor(self):
        """ Moves the cursor up and down if you pressed the corresponding key """
        if self.interface.DOWN_KEY:     # If they pressed the Down arrow key
            if self.cursor.rect.y != self.rules_button.rect.y:     # Stops the cursor from moving above/below button
                self.cursor.rect.y += 160   # Moves the cursor up and down
                pygame.mixer.Sound.play(self.menu_sound)

        elif self.interface.UP_KEY:
            if self.cursor.rect.y != self.play_button.rect.y:
                self.cursor.rect.y -= 160
                pygame.mixer.Sound.play(self.menu_sound)

    def check_input(self):
        """ Checks if they pressed a key """
        self.move_cursor()

        if self.interface.ENTER_KEY:    # If they pressed enter
            pygame.mixer.Sound.play(self.menu_sound)

            for button in self.button_list:     # Finds the button selected
                if button.rect.y == self.cursor.rect.y:     # If the cursor rect overlaps with that button
                    if button == self.play_button:
                        self.interface.current_screen = self.interface.game_mode    # Changes to game mode menu
                        self.run_display = False

                    elif button == self.option_button:
                        self.interface.current_screen = self.interface.options
                        self.run_display = False

                    elif button == self.rules_button:
                        webbrowser.open(r"https://www.ultraboardgames.com/uno/game-rules.php")



class Options(Menu):
    def __init__(self, interface):
        super().__init__(interface)

        self.volume_label = self.button_font.render("Volume", True, (255, 255, 255))
        self.volume_button = Button(self.MID_W - 400, self.MID_H - 135, 240, 70)

        self.volume_slider = Button(self.MID_W - 130, self.MID_H - 100, 500, 7)
        self.volume_slider.active = True
        self.volume_slider.colour = self.volume_slider.colour_active

        self.volume = 0.5
        self.volume_circle_x = 120

        self.sound_label = self.button_font.render("Sound", True, (255, 255, 255))
        self.sound_button = Button(self.MID_W - 400, self.MID_H, 240, 70)

        self.sound = Button(self.volume_slider.rect.centerx - 50, self.MID_H, 100, 70)

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0, 0, 0))

            self.menu_sound.set_volume(self.interface.volume)
            if self.sound.active:
                self.interface.volume = 0

            self.interface.check_events()
            self.check_input()

            self.interface.screen.blit(self.volume_label,
                                       (self.volume_button.rect.centerx - self.volume_label.get_width() / 2,
                                        self.volume_button.rect.centery - self.volume_label.get_height() / 2))

            self.interface.screen.blit(self.sound_label,
                                       (self.sound_button.rect.centerx - self.sound_label.get_width() / 2,
                                        self.sound_button.rect.centery - self.sound_label.get_height() / 2))

            self.volume_button.draw_rect(self.interface.screen)
            self.sound_button.draw_rect(self.interface.screen)

            self.volume_slider.draw_rect(self.interface.screen)
            self.sound.draw_rect(self.interface.screen)

            pygame.draw.circle(self.interface.screen, (255, 255, 255), (self.MID_W + self.volume_circle_x,
                                                                        self.volume_slider.rect.centery), 20)

            if self.sound.active:
                pygame.draw.line(self.interface.screen, (255, 255, 255),
                                 (self.sound.rect.topleft), (self.sound.rect.bottomright), 3)
                pygame.draw.line(self.interface.screen, (255, 255, 255),
                                 (self.sound.rect.topright), (self.sound.rect.bottomleft), 3)

            self.blit_description()

            self.interface.clock.tick(60)   # 60 fps
            pygame.display.update()
            self.reset_keys()

    def check_input(self):   # Create sliders or options later
        if self.interface.BACK_KEY:
            pygame.mixer.Sound.play(self.menu_sound)
            self.interface.current_screen = self.interface.main_menu
            self.run_display = False

        elif self.interface.LEFT_KEY and self.volume_slider.active and (self.MID_W + self.volume_circle_x !=
                                                                        self.MID_W - 130):
            pygame.mixer.Sound.play(self.menu_sound)
            self.volume_circle_x -= 50
            self.volume -= 0.1      # Decrease the volume

            if not self.sound.active:   # Only changes the volume if the player has enabled the sound
                self.interface.volume = self.volume

        elif self.interface.RIGHT_KEY and self.volume_slider.active and (self.MID_W + self.volume_circle_x !=
                                                                         self.MID_W + 370):
            pygame.mixer.Sound.play(self.menu_sound)
            self.volume_circle_x += 50
            self.volume += 0.1      # Increase the volume

            if not self.sound.active:
                self.interface.volume = self.volume

        elif self.interface.UP_KEY and self.sound.colour == self.sound.colour_active:
            pygame.mixer.Sound.play(self.menu_sound)
            self.volume_slider.active = True
            self.volume_slider.colour = self.volume_slider.colour_active

            self.sound.colour = self.sound.colour_passive

        elif self.interface.DOWN_KEY and self.volume_slider.active:
            pygame.mixer.Sound.play(self.menu_sound)
            self.sound.colour = self.sound.colour_active

            self.volume_slider.active = False
            self.volume_slider.colour = self.volume_slider.colour_passive

        elif self.interface.ENTER_KEY and self.sound.colour == self.sound.colour_active:
            if self.sound.active:   # To enable or disable the sound
                self.sound.active = False
                self.interface.volume = self.volume
            else:
                self.sound.active = True
                self.interface.volume = 0

class GameMode(Menu):
    def __init__(self, interface):
        super().__init__(interface)
        self.waiting = False

        self.waiting_text = self.button_font.render("Waiting For Other Players", True, (255, 255, 255))

        self.two_player_label = self.button_font.render("Two Player", True, (255, 255, 255))
        self.two_player_button = Button(self.MID_W - 150, self.MID_H - 120, 300, 80)  # x, y, width, height

        self.three_player_label = self.button_font.render("Three Player", True, (255, 255, 255))
        self.three_player_button = Button(self.MID_W - 150, self.MID_H, 300, 80)

        self.four_player_label = self.button_font.render("Four Player", True, (255, 255, 255))
        self.four_player_button = Button(self.MID_W - 150, self.MID_H + 120, 300, 80)

        self.cursor = Button(self.MID_W - 150, self.MID_H, 300, 80)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.two_player_button, self.three_player_button, self.four_player_button, self.cursor]

        self.start_sound = pygame.mixer.Sound("Sounds\start sound.ogg")

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.menu_sound.set_volume(self.interface.volume)
            self.start_sound.set_volume(self.interface.volume)

            self.interface.screen.blit(self.two_player_label, (self.MID_W - self.two_player_label.get_width() / 2,
                                                               self.MID_H - 100))
            self.interface.screen.blit(self.three_player_label, (self.MID_W - self.three_player_label.get_width() / 2,
                                                                 self.MID_H + 20))
            self.interface.screen.blit(self.four_player_label, (self.MID_W - self.four_player_label.get_width() / 2,
                                                                self.MID_H + 140))

            self.blit_description()

            self.interface.check_events()
            self.check_input()

            for b in self.button_list:
                b.draw_rect(self.interface.screen)

            pygame.display.update()
            self.interface.clock.tick(60)   # 60 fps
            self.reset_keys()

    def move_cursor(self):
        if self.interface.DOWN_KEY:
            if self.cursor.rect.y != self.four_player_button.rect.y:    # Stops the cursor from moving away from buttons
                self.cursor.rect.y += 120
                pygame.mixer.Sound.play(self.menu_sound)

        if self.interface.UP_KEY:
            if self.cursor.rect.y != self.two_player_button.rect.y:
                self.cursor.rect.y -= 120
                pygame.mixer.Sound.play(self.menu_sound)

    def check_input(self):
        self.move_cursor()

        if self.interface.ENTER_KEY:    # If they pressed enter
            for button in self.button_list:     # Finds the button selected
                if button.rect.y == self.cursor.rect.y:     # If the cursor rect overlaps with that button

                    if button == self.two_player_button:    # Sets the chosen game mode to a variable
                        self.interface.game_mode_choice = 2     # Their choice will be sent to the server after

                    elif button == self.three_player_button:
                        self.interface.game_mode_choice = 3

                    elif button == self.four_player_button:
                        self.interface.game_mode_choice = 4

                    self.run_display = False
                    pygame.mixer.Sound.play(self.start_sound)

        elif self.interface.BACK_KEY:   # Goes back to the main menu
            self.interface.current_screen = self.interface.main_menu
            self.run_display = False
            pygame.mixer.Sound.play(self.menu_sound)

    def waiting_screen(self):
        """ This is displayed while you wait for other players to join """
        self.interface.screen.fill((0,0,0))
        self.interface.check_events()
        self.interface.screen.blit(self.waiting_text, (self.MID_W - self.waiting_text.get_width() / 2,
                                                       self.MID_H - self.waiting_text.get_height() / 2))

        pygame.display.update()
        self.interface.clock.tick(60)   # 60 fps
        self.reset_keys()


















