import pygame
from button import Button
from deck import Deck, Images
from actions import *


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

    def reset_keys(self):
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

        self.title = self.title_font.render("Uno", True, (255, 255, 255))

        # x, y for top left corner of the rectangle and then width, height
        self.play_button = Button(self.MID_W - 160, self.MID_H - 80, 320, 100)
        self.option_button = Button(self.MID_W - 160, self.MID_H + 80, 320, 100)

        self.cursor = Button(self.MID_W - 160, self.MID_H - 80, 320, 100)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.play_button, self.option_button, self.cursor]

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))

            self.interface.screen.blit(self.title, (self.MID_W - self.title.get_width() / 2,    # This centres the text
                                       self.MID_H - 320))
            self.interface.screen.blit(self.play_label, (self.MID_W - self.play_label.get_width() / 2,
                                        self.MID_H - 60))
            self.interface.screen.blit(self.option_label, (self.MID_W - self.option_label.get_width() / 2,
                                       self.MID_H + 100))

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

        elif self.interface.UP_KEY:
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

    def display(self):
        self.run_display = True
        while self.run_display:
            self.interface.screen.fill((0,0,0))
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

                    if button == self.two_player_button:    # Sets the chosen game mode to a variable
                        self.interface.game_mode_choice = 2     # Their choice will be sent to the server after

                    elif button == self.three_player_button:
                        self.interface.game_mode_choice = 3

                    elif button == self.four_player_button:
                        self.interface.game_mode_choice = 4

                    self.run_display = False
                    #self.waiting = True     # So the client calls the waiting_screen method


        elif self.interface.BACK_KEY:   # Goes back to the main menu
            self.interface.current_screen = self.interface.main_menu
            self.run_display = False


    def waiting_screen(self):
        """ This is displayed while you wait for other players to join """
        self.interface.screen.fill((0,0,0))
        self.interface.screen.blit(self.waiting_text, (self.MID_W - self.waiting_text.get_width() / 2,
                                                       self.MID_H - self.waiting_text.get_height() / 2))

        pygame.display.update()
        self.interface.clock.tick(60)   # 60 fps


class Image:
    def __init__(self, image):
        self.image = image
        self.x = None
        self.y = None
        self.rect = None

class GameScreen(Menu):
    def __init__(self, interface):
        super().__init__(interface)

        self.dk = Deck()
        self.dk.create_deck()

        self.offset = -320
        self.opponent_x_offset = -480
        self.opponent_y_offset = -340

        self.b_img = pygame.image.load(Images().card_back).convert_alpha()
        self.back_image = pygame.transform.scale(self.b_img, (self.b_img.get_width() * 0.22,
                                                              self.b_img.get_height() * 0.22))
        self.confirm = False
        self.cursor = Button(self.MID_W + 400, self.MID_H, 300, 80)
        self.cursor.colour = self.cursor.colour_active

        self.yes_button = Button(self.MID_W - 400, self.MID_H, 300, 80)
        self.yes_text = self.button_font.render("Yes", True, (255, 255, 255))
        self.no_button = Button(self.MID_W + 400, self.MID_H, 300, 80)
        self.no_text = self.button_font.render("No", True, (255, 255, 255))

        self.choice = None
        self.chosen_card = None
        self.deck = None
        self.action = None
        self.player_id = None
        self.game = None

        self.image_list = []

        self.add_image(self.dk.deck[0])   # Creating a temporary image which is used to create cursor
        # Create a rectangle with same width and height as the card image
        self.cursor_rect = self.image_list[0].image.get_rect(topleft=(self.MID_W + self.offset, self.MID_H + 270))
        self.image_list.pop()   # Remove the temp image

    def create_images(self):
        """ Creates the images for all the cards in your deck """
        for card in self.deck:
            self.add_image(card)

    def add_image(self, card):
        """ Gets the image from the image attribute in the card object and scales it """
        img = pygame.image.load(card.image).convert_alpha()
        # Change size of image
        scaled_image = pygame.transform.scale(img, (img.get_width() * 0.3, img.get_height() * 0.3))
        self.image_list.append(Image(scaled_image))  # Create Image object and add it to list

    def reset_offsets(self):
        """ To display the cards in the correct position in the next loop of the while loop """
        self.offset = -320
        self.opponent_x_offset = -480
        self.opponent_y_offset = -340

    def display(self, player_id, game):
        self.player_id = player_id
        self.game = game
        self.interface.screen.fill((0, 0, 0))

        self.deck = self.game.player_list[player_id].deck
        self.create_images()

        left_opponent = game.player_list[(player_id + 1) % len(game.player_list)]   # To return to the start of the list if needed
        # e.g In 3 player mode, if it's player 2, the left becomes player 0: (2+1) % 3 = 0
        right_opponent = game.player_list[player_id - 1]

        for image in self.image_list:   # Go through image objects in the image_list and set their co-ordinates
            self.interface.screen.blit(image.image, (self.MID_W + self.offset, self.MID_H + 270))  # Blit your cards

            image.x = self.MID_W + self.offset   # Assign the x and y attributes values
            image.y = self.MID_H + 270
            image.rect = image.image.get_rect(topleft=(image.x, image.y))  # Create a rect of the same size as the image
            self.offset += 90

        if self.chosen_card:     # Put the chosen card in the centre of screen
            self.interface.screen.blit(self.chosen_card, (self.MID_W - self.chosen_card.get_width() / 2,
                                                          self.MID_H - self.chosen_card.get_height() / 2))

        for i in range(0, len(left_opponent.deck)):     # Display the opponent's cards faced down
            self.interface.screen.blit(self.back_image,
                                       (self.MID_W + self.opponent_x_offset, self.MID_H + self.opponent_y_offset))
            self.opponent_y_offset += 60    # So the cards move downwards

        self.opponent_x_offset = 400   # To blit on the right side of the screen
        self.opponent_y_offset = -340   # Reset it

        for j in range(0, len(right_opponent.deck)):
            self.interface.screen.blit(self.back_image, (self.MID_W + self.opponent_x_offset,
                                                         self.MID_H + self.opponent_y_offset))
            self.opponent_y_offset += 60    # So the cards move downwards

        if self.game.turn == self.player_id:    # Allows them to select a card if it's their turn
            # Draw the cursor rectangle; 2 blits the border only
            pygame.draw.rect(self.interface.screen, pygame.Color("black"), self.cursor_rect, 2)

            self.interface.check_events()
            self.check_input()
            self.reset_keys()   # Allows the user to press another key

        else:   # If it's not their turn, they cannot perform any actions
            pass    # Display "Opponent's turn"?

        self.interface.clock.tick(60)   # 60 fps
        pygame.display.update()

        self.reset_offsets()
        self.image_list = []    # Reset it since the user may have drawn or placed down a card

    def move_cursor(self):
        if self.interface.LEFT_KEY:     # If they pressed left or right
            if self.cursor_rect.x != self.image_list[0].rect.x:  # If the cursor is not on the left-most image
                self.cursor_rect.x -= 90    # Moves the cursor rectangle
        elif self.interface.RIGHT_KEY:
            if self.cursor_rect.x != self.image_list[-1].rect.x:  # If the cursor is not on the left-most image
                self.cursor_rect.x += 90

    def check_input(self):
        self.move_cursor()

        if self.interface.ENTER_KEY: #and self.player_id == self.game.turn:
            for image in self.image_list:
                if self.cursor_rect.x == image.rect.x:   # If the cursor overlaps with the image's rectangle
                    card_index = self.image_list.index(image)    # The position of the chosen image in the list
                    self.choose_card(card_index)    # Uses the index to check if that card in the deck is valid

                    if self.interface.card_chosen:
                        self.deck.pop(card_index)   # So the card doesn't get displayed among your deck

                    else:   # The card they pick does not match in colour or value
                        pass    # They are prompted to choose another card

        else:
            pass    # Display "Not ur turn" on screen

    def ask(self):
        """ Asks the user if they want to place their drawn card down """
        self.interface.screen.fill((0, 0, 0))
        self.interface.screen.blit(self.yes_text, (self.MID_W - 250,    # Drawing the text and buttons onto screen
                                                   self.MID_H - 100))
        self.interface.screen.blit(self.no_text, (self.MID_W + 250,
                                                  self.MID_H - 100))
        self.yes_button.draw_rect(self.interface.screen)
        self.no_button.draw_rect(self.interface.screen)

        if self.interface.LEFT_KEY:     # Moves the cursor rect so you can select an option
            if self.cursor.rect.x != self.no_button.rect.x:  # If it's not already on the no button
                self.cursor.rect.x -= 800
        elif self.interface.RIGHT_KEY:
            if self.cursor.rect.x != self.yes_button.rect.x:
                self.cursor.rect.x += 800

        elif self.interface.ENTER_KEY:
            if self.cursor.rect.x == self.yes_button.rect.x:
                self.action = Decision("Yes")
            else:
                self.action = Decision("No")

            self.confirm = False    # To stop the loop in the client

        self.cursor.draw_rect(self.interface.screen)
        pygame.display.update()

    def choose_card(self, choice):
        """ To choose your own card """
        # Add the draw card option

        current_player = self.game.player_list[self.player_id]

        if (current_player.deck[choice].colour == self.game.discard_pile[-1].colour) or \
                (current_player.deck[choice].value == self.game.discard_pile[-1].value):  # Not valid
            self.action = PlaceCard(choice)
            self.interface.card_chosen = True
            self.chosen_card = self.image_list[choice].image

        elif current_player.deck[choice].colour == None:   # wildcard
            new_colour = input("Choose a colour for the next player: ")
            self.action = PlaceCard(choice, colour=new_colour)  # Colour is an optional parameter
            self.interface.card_chosen = True
            self.chosen_card = self.image_list[choice].image

        # else: # Prompt to choose another card












