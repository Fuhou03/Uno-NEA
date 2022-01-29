import pygame
from button import Button
from deck import Deck #
import random #


class Menu:
    def __init__(self, interface):
        self.interface = interface
        self.run_display = True

        #self.MID_W, self.MID_H = 390, 350
        self.MID_W, self.MID_H = (self.interface.SCREEN_W / 2), (self.interface.SCREEN_H / 2)

        self.menu_font = pygame.font.Font(None, 100)
        self.text_font = pygame.font.Font(None, 40)
        self.button_font = pygame.font.Font(None, 60)

        self.enter_desc = self.text_font.render("Enter To Select", True, (255, 255, 255))
        self.back_desc = self.text_font.render("Backspace To Return", True, (255, 255, 255))
        self.arrow_desc = self.text_font.render("Arrows To Navigate", True, (255, 255, 255))

    def reset_keys(self):
        self.interface.ENTER_KEY = False
        self.interface.BACK_KEY = False
        self.interface.DOWN_KEY = False
        self.interface.UP_KEY = False

    def blit_description(self):
        self.interface.screen.blit(self.enter_desc, (self.MID_W + 300, self.MID_H + 400))
        self.interface.screen.blit(self.back_desc, (self.MID_W - 520, self.MID_H + 400))
        self.interface.screen.blit(self.arrow_desc, (self.MID_W - 100, self.MID_H + 400))

class MainMenu(Menu):
    def __init__(self, interface):      # Having interface as an argument allows us to its variables and the screen
        super().__init__(interface)     # Inherit from Menu class to access its attributes and methods
        self.title_font = pygame.font.Font(None, 170)
        self.play_label = self.menu_font.render("Play", True, (255, 255, 255))
        self.option_label = self.menu_font.render("Options", True, (255, 255, 255))

        self.title = self.title_font.render("Uno", True, (255, 255, 255))

        # x, y for top left corner of the rectangle and then width, height
        self.play_button = Button(self.MID_W - 150, self.MID_H - 80, 320, 100)
        self.option_button = Button(self.MID_W - 150, self.MID_H + 80, 320, 100)

        self.cursor = Button(self.MID_W - 150, self.MID_H - 80, 320, 100)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.play_button, self.option_button, self.cursor]

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.title, (self.MID_W - 100, self.MID_H - 320))
            self.interface.screen.blit(self.play_label, (self.MID_W - 65, self.MID_H - 60))
            self.interface.screen.blit(self.option_label, (self.MID_W - 130, self.MID_H + 100))

            self.blit_description()

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
                self.cursor.rect.y += 160   # Moves the cursor up and down

        if self.interface.UP_KEY:
            if self.cursor.rect.y != self.play_button.rect.y:
                self.cursor.rect.y -= 160

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
        self.volume_button = Button(self.MID_W - 400, self.MID_H + 120, 240, 70)

        self.music_label = self.button_font.render("Music", True, (255, 255, 255))
        self.music_button = Button(self.MID_W - 400, self.MID_H, 240, 70)

        self.sound_label = self.button_font.render("Sound", True, (255, 255, 255))
        self.sound_button = Button(self.MID_W - 400, self.MID_H - 120, 240, 70)

        self.button_list = [self.volume_button, self.music_button, self.sound_button]


    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.volume_label, (self.MID_W - 350, self.MID_H - 100))
            self.interface.screen.blit(self.music_label, (self.MID_W - 345, self.MID_H + 20))
            self.interface.screen.blit(self.sound_label, (self.MID_W - 345, self.MID_H + 140))

            self.blit_description()

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
        self.running = True
        self.waiting_text = self.button_font.render("Waiting For Other Players", True, (255, 255, 255))

        self.two_player_label = self.button_font.render("Two Player", True, (255, 255, 255))
        self.two_player_button = Button(self.MID_W - 150, self.MID_H - 120, 300, 80)  # x, y, width, height

        self.three_player_label = self.button_font.render("Three Player", True, (255, 255, 255))
        self.three_player_button = Button(self.MID_W - 150, self.MID_H, 300, 80)

        self.four_player_label = self.button_font.render("Four Player", True, (255, 255, 255))
        self.four_player_button = Button(self.MID_W - 150, self.MID_H + 120, 300, 80)

        self.cursor = Button(self.MID_W - 150, self.MID_H - 120, 300, 80)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.two_player_button, self.three_player_button, self.four_player_button, self.cursor]

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.two_player_label, (self.MID_W - 120, self.MID_H - 100))
            self.interface.screen.blit(self.three_player_label, (self.MID_W - 130, self.MID_H + 20))
            self.interface.screen.blit(self.four_player_label, (self.MID_W - 116, self.MID_H + 136))

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
            if self.cursor.rect.y != self.four_player_button.rect.y:     # Stops the cursor from moving away from buttons
                self.cursor.rect.y += 240

        if self.interface.UP_KEY:
            if self.cursor.rect.y != self.two_player_button.rect.y:
                self.cursor.rect.y -= 240


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
                    self.interface.current_screen = self.interface.game_display
                    #self.interface.running = False
                    #pygame.quit()      # To close the window
                    #self.waiting()



        elif self.interface.BACK_KEY:   # Goes back to the main menu
            self.interface.current_screen = self.interface.main_menu
            self.run_display = False


    def waiting(self):
        while self.running:
            self.interface.screen.fill((0,0,0))
            self.interface.screen.blit(self.waiting_text, (self.MID_W, self.MID_H + 15))

            pygame.display.update()
            self.interface.clock.tick(60)   # 60 fps


class GameDisplay(Menu):
    def __init__(self, interface):
        super().__init__(interface)
        self.dk = Deck()
        self.dk.create_deck()

        self.offset = -320
        self.opponent_x_offset = -480
        self.opponent_y_offset = -340


    def display(self):
        self.run_display = True
        done = False

        while self.run_display:
            self.interface.screen.fill((0, 0, 0))
            random.shuffle(self.dk.deck)
            new_deck = self.dk.deck[:7]

            centre = self.button_font.render("Centre", True, (255, 255, 255))
            self.interface.screen.blit(centre, (self.MID_W - 30, self.MID_H))

            if not done:
                for card in new_deck:
                    img = pygame.image.load(card.image).convert_alpha()
                    width = img.get_width()
                    height = img.get_height()
                    image = pygame.transform.scale(img, ((width * 0.3), (height * 0.3)))    # Change size of image
                    self.interface.screen.blit(image, (self.MID_W + self.offset, self.MID_H + 270))
                    self.offset += 90

                b_img = pygame.image.load(self.dk.images.card_back).convert_alpha()
                back_width = b_img.get_width()
                back_height = b_img.get_height()
                back_image = pygame.transform.scale(b_img, ((back_width * 0.22), (back_height * 0.22)))

                for i in range(2):  # For both sides of the screen
                    for j in range(7):
                        self.interface.screen.blit(back_image, (self.MID_W + self.opponent_x_offset,
                                                                self.MID_H + self.opponent_y_offset))
                        self.opponent_y_offset += 60    # So the cards move downwards
                    self.opponent_x_offset = 400   # Multiply by -1 to blit on the right side of screen
                    self.opponent_y_offset = -340   # Reset

                pygame.display.update()
                done = True

                #img_rect = self.img.get_rect()


            #self.interface.check_events()
            #self.check_input()

            #for b in self.button_list:
            #b.draw_rect(self.interface.screen)


            #self.interface.clock.tick(60)   # 60 fps
            #self.reset_keys()

    def check_input(self):
        pass








