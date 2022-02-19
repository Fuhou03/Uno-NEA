import pygame
from button import Button
from deck import Images
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

        self.title = self.title_font.render("Uno", True, (255, 255, 255))

        # x, y for top left corner of the rectangle and then width, height
        self.play_button = Button(self.MID_W - 160, self.MID_H - 80, 320, 100)
        self.option_button = Button(self.MID_W - 160, self.MID_H + 80, 320, 100)

        self.cursor = Button(self.MID_W - 160, self.MID_H - 80, 320, 100)
        self.cursor.colour = self.cursor.colour_active

        self.button_list = [self.play_button, self.option_button, self.cursor]

    def display(self):
        """ Displays the text and buttons and checks if they pressed a key """
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
        """ Moves the cursor up and down if you pressed the corresponding key """
        if self.interface.DOWN_KEY:     # If they pressed the Down arrow key
            if self.cursor.rect.y != self.option_button.rect.y:     # Stops the cursor from moving above/below button
                self.cursor.rect.y += 160   # Moves the cursor up and down

        elif self.interface.UP_KEY:
            if self.cursor.rect.y != self.play_button.rect.y:
                self.cursor.rect.y -= 160

    def check_input(self):
        """ Checks if they pressed a key """
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

        elif self.interface.BACK_KEY:   # Goes back to the main menu
            self.interface.current_screen = self.interface.main_menu
            self.run_display = False

    def waiting_screen(self):
        """ This is displayed while you wait for other players to join """
        self.interface.screen.fill((0,0,0))
        self.interface.check_events()
        self.interface.screen.blit(self.waiting_text, (self.MID_W - self.waiting_text.get_width() / 2,
                                                       self.MID_H - self.waiting_text.get_height() / 2))

        pygame.display.update()
        self.interface.clock.tick(60)   # 60 fps
        self.reset_keys()


class Image:
    def __init__(self, image, **kw):
        self.image = image
        self.x = None
        self.y = None
        self.colour = kw.get("colour")

class GameScreen(Menu):
    def __init__(self, interface):
        super().__init__(interface)

        self.offset = -320
        self.opponent_x_offset = -480
        self.opponent_y_offset = -340

        self.b_img = pygame.image.load(Images().card_back).convert_alpha()
        self.back_image = pygame.transform.scale(self.b_img, (self.b_img.get_width() * 0.22,
                                                              self.b_img.get_height() * 0.22))

        self.red_d = pygame.image.load(Images().red_diamond).convert_alpha()
        self.blue_d = pygame.image.load(Images().blue_diamond).convert_alpha()
        self.green_d = pygame.image.load(Images().green_diamond).convert_alpha()
        self.yellow_d = pygame.image.load(Images().yellow_diamond).convert_alpha()

        self.draw_button = Button(self.MID_W - 100, self.MID_H + 185, 200, 60)
        self.draw_text = self.text_font.render("Draw", True, (255, 255, 255))

        self.confirm = False
        self.ask_cursor = Button(self.MID_W + 100, self.MID_H + 100, 300, 80)
        self.ask_cursor.colour = self.ask_cursor.colour_active

        self.yes_button = Button(self.MID_W + 100, self.MID_H + 100, 300, 80)
        self.yes_text = self.button_font.render("Yes", True, (255, 255, 255))
        self.no_button = Button(self.MID_W - 400, self.MID_H + 100, 300, 80)
        self.no_text = self.button_font.render("No", True, (255, 255, 255))

        self.deck = None        # Assigned later
        self.action = None
        self.player_id = None
        self.game = None
        self.colour_cursor = None
        self.new_colour = None
        self.choosing_colour = False
        self.invalid = False

        self.left_opponent = None
        self.right_opponent = None
        self.top_opponent = None
        self.TOP_ID = None

        self.image_list = []
        self.image_list_length = 7
        self.number_of_cards_changed = False
        self.total_image_width = None   # Used to center all your images
        self.cursor_rect = None

    def create_images(self):
        """ Creates the images for all the cards in your deck """
        self.image_list = []
        for card in self.deck:
            self.image_list.append(Image(self.scale_image(card))) # Create Image object and add it to list

    def scale_image(self, card):
        """ Gets the image from the image attribute in the card object and scales it """
        img = pygame.image.load(card.image).convert_alpha()
        # Change size of image
        scaled_image = pygame.transform.scale(img, (img.get_width() * 0.3, img.get_height() * 0.3))
        return scaled_image

    def display_direction(self):
        """ Display the direction image onto screen """

        clockwise = pygame.image.load(Images().clockwise).convert_alpha()
        clockwise_img = pygame.transform.scale(clockwise, (clockwise.get_width() * 0.15, clockwise.get_height() * 0.15))

        anticlockwise = pygame.image.load(Images().anticlockwise).convert_alpha()
        anticlockwise_img = pygame.transform.scale(anticlockwise, (anticlockwise.get_width() * 0.40,
                                                                   anticlockwise.get_height() * 0.40))

        CW_X, ACW_X = self.MID_W - clockwise_img.get_width() / 2, self.MID_W - anticlockwise_img.get_width() / 2
        CW_Y, ACW_Y = self.MID_H - clockwise_img.get_height() / 2, self.MID_H - anticlockwise_img.get_height() / 2

        if self.TOP_ID != None:     # 2 or 4 player mode
            CW_X += 200
            ACW_X += 200
        else:   # The direction arrow image is in a different position for 3 player mode
            CW_Y -= 220
            ACW_Y -= 220

        if self.game.direction == "clockwise":
            self.interface.screen.blit(clockwise_img, (CW_X, CW_Y))
        else:
            self.interface.screen.blit(anticlockwise_img, (ACW_X, ACW_Y))

    def display_player_info(self):
        """ Display the current player and the player number of each player """
        turn_text = self.button_font.render("Current Turn: P" + str(self.game.turn), True, (255, 255, 255))

        my_id_text = self.button_font.render("P" + str(self.player_id), True, (255, 255, 255))
        self.interface.screen.blit(my_id_text, (self.MID_W - my_id_text.get_width() / 2, self.MID_H + 125))

        if self.game.game_mode == 2:
            self.TOP_ID = (self.player_id + 1) % len(self.game.player_list)  # Either 0 or 1

        else:
            if self.game.game_mode == 4:    # E.g. The top player will be P1 if you're P3, or P2 if you're P4
                self.TOP_ID = self.game.player_list.index(self.game.player_list[self.player_id - 2])

            # The player id's of the opponents
            LEFT_ID = (self.player_id + 1) % len(self.game.player_list)     # % To get the 1st index when needed
            # e.g In 3 player mode, if it's player 2, the left becomes player 0: (2+1) % 3 = 0

            # If you are P0 the right opponent will be P2 instead of P -1 (no -ve index)
            RIGHT_ID = self.game.player_list.index(self.game.player_list[self.player_id - 1])

            self.left_opponent = self.game.player_list[LEFT_ID]
            self.right_opponent = self.game.player_list[RIGHT_ID]

            right_text = self.button_font.render("P" + str(RIGHT_ID), True, (255, 255, 255))
            left_text = self.button_font.render("P" + str(LEFT_ID), True, (255, 255, 255))

            self.interface.screen.blit(right_text, (self.MID_W + 410, self.MID_H - 380))
            self.interface.screen.blit(left_text, (self.MID_W - 460, self.MID_H - 380))

        if self.TOP_ID != None:  # If it's game mode 2 or 4 then there is a player at the top
            self.top_opponent = self.game.player_list[self.TOP_ID]
            top_text = self.button_font.render("P" + str(self.TOP_ID), True, (255,255,255))
            self.interface.screen.blit(top_text, (self.MID_W - top_text.get_width() / 2, self.MID_H - 380))

            self.interface.screen.blit(turn_text, (self.MID_W - turn_text.get_width() / 2, self.MID_H - 480))
        else:
            self.interface.screen.blit(turn_text, (self.MID_W - turn_text.get_width() / 2, self.MID_H - 380))

        # If a player put a wildcard down, display the colour that was chosen for the next player
        if self.game.discard_pile[-1].value == "wild" or self.game.discard_pile[-1].value == "wild 4":
            colour_text = self.text_font.render("Colour Chosen: " + self.game.discard_pile[-1].colour,
                                                  True, (255, 255, 255))
            if self.TOP_ID != None:     # 2/4 P Mode uses different coordinates
                self.interface.screen.blit(colour_text, (self.MID_W - colour_text.get_width() / 2, self.MID_H - 430))
            else:
                self.interface.screen.blit(colour_text, (self.MID_W - colour_text.get_width() / 2, self.MID_H - 335))

    def display_center_card(self):
        """ Display in the centre the card placed at the top of the discard pile """
        top_card = Image(self.scale_image(self.game.discard_pile[-1]))  # Create an image object
        top_card_img = top_card.image  # Get the image from that card
        self.interface.screen.blit(top_card_img, (self.MID_W - top_card_img.get_width() / 2,
                                                  self.MID_H - top_card_img.get_height() / 2))

    def reset_offsets(self):
        """ To display the cards in the correct position in the next loop of the while loop """
        self.offset = 0
        self.opponent_x_offset = -480
        self.opponent_y_offset = -320

    def display_opponents_cards(self):
        """ Displaying the opponent's cards faced down """

        if self.game.game_mode != 2:
            for i in range(0, len(self.left_opponent.deck)):
                self.interface.screen.blit(self.back_image,
                                           (self.MID_W + self.opponent_x_offset, self.MID_H + self.opponent_y_offset))
                self.opponent_y_offset += 50    # So the cards move downwards

            self.reset_offsets()    # Reset it for the other opponent
            self.opponent_x_offset = 480 - self.back_image.get_width()    # To blit the cards of the opponent on the right

            for j in range(0, len(self.right_opponent.deck)):
                self.interface.screen.blit(self.back_image, (self.MID_W + self.opponent_x_offset,
                                                             self.MID_H + self.opponent_y_offset))
                self.opponent_y_offset += 50    # So the cards move downwards

        if self.game.game_mode == 2 or self.game.game_mode == 4:
            image_width = self.back_image.get_width() * len(self.top_opponent.deck) - \
                          ((self.back_image.get_width() - 60) * len(self.top_opponent.deck))

            top_offset = 0
            for i in range(0, len(self.top_opponent.deck)):
                self.interface.screen.blit(self.back_image,
                                           ((self.MID_W - image_width / 2) + top_offset, self.MID_H - 320))
                top_offset += 50

    def display_your_cards(self):
        """ Displaying your cards on the screen """
        # The length from the left side of your first card to the right side of your last card (To keep them centered)

        self.total_image_width = (self.image_list[0].image.get_width() * len(self.image_list)) - \
                                 ((self.image_list[0].image.get_width() - 90) * len(self.image_list))
        for img in self.image_list:   # Go through the Image objects in the image_list and set their co-ordinates
            # Blit your cards   # self.offset is 0 initially then is incremented each time so the cards overlap
            # You cannot get an image's co-ordinates so I assigned their co-ordinates to an attribute to use them later
            img.x = self.MID_W - (self.total_image_width / 2) + self.offset
            img.y = self.MID_H + 270  # Assign values to the Image object's x and y attributes

            self.interface.screen.blit(img.image, (img.x, img.y))
            self.offset += 90

    def display(self, player_id, game):
        """ Displays all the cards onto the screen and allows you to select a card if it's your turn """
        self.player_id = player_id
        self.game = game
        self.interface.screen.fill((0, 100, 255))
        self.interface.check_events()   # Check for key presses

        self.deck = self.game.player_list[self.player_id].deck
        self.create_images()    # Getting images for every card in your deck

        self.display_player_info()
        self.display_direction()

        if len(self.image_list) != self.image_list_length:  # A card was placed down or drawn
            self.image_list_length = len(self.image_list)    # Used to adjust the cursor rect coordinates
            self.number_of_cards_changed = True

        self.display_opponents_cards()
        self.display_your_cards()
        self.display_center_card()

        self.draw_button.draw_rect(self.interface.screen)   # Put draw button and text onto screen
        self.interface.screen.blit(self.draw_text, (self.MID_W - self.draw_text.get_width() / 2, self.MID_H + 205))

        # Allows them to select a card if it's their turn
        if self.game.turn == self.player_id:
            # Draw the cursor rectangle; 2 blits the border only
            if not self.cursor_rect or self.number_of_cards_changed:    # Create the rectangle
                self.cursor_rect = self.image_list[0].image.get_rect(topleft=(self.MID_W - (self.total_image_width / 2),
                                                                          self.MID_H + 270))
                self.number_of_cards_changed = False

            pygame.draw.rect(self.interface.screen, pygame.Color("black"), self.cursor_rect, 2)
            self.check_input()      # Checks for key presses and lets them move the cursor and select a card

            if self.invalid:    # If the card they chose cannot be placed down
                invalid_text = self.text_font.render("Choose Another Card", True, (255, 255, 255))
                self.interface.screen.blit(invalid_text, (self.MID_W - invalid_text.get_width() / 2, self.MID_H - 130))

        else:   # If it's not their turn, they cannot perform any actions as there is no cursor rectangle
            pass

        self.interface.clock.tick(60)   # 60 fps
        pygame.display.update()
        self.reset_keys()   # Allows the user to press another key
        self.reset_offsets()
        self.image_list = []    # Reset it since the user may have drawn or placed down a card

    def choose_card(self, choice):
        """ Checks if your chosen card is valid and adds your selected card into an action object """
        # Add the draw card option

        current_player = self.game.player_list[self.player_id]

        if current_player.deck[choice].colour == None:   # If they chose a wildcard (it has no colour)
            self.choosing_colour = True
            self.reset_keys()
            while self.choosing_colour:     # Lets the user select the next colour
                self.choose_colour()

            # Display the chosen colour
            self.action = PlaceCard(choice, colour=self.new_colour)  # Colour is an optional parameter
            self.interface.card_chosen = True
            self.new_colour = None  # Reset

        elif (current_player.deck[choice].colour == self.game.discard_pile[-1].colour) or \
                (current_player.deck[choice].value == self.game.discard_pile[-1].value):  # If they chose any other card
            self.action = PlaceCard(choice)
            self.interface.card_chosen = True

        else:   # The card they pick does not match in colour or value
            self.invalid = True     # They will be asked to choose another card

    def move_cursor(self):
        """ Move the cursor rectangle left or right to select a card, or up and down to press the 'Draw' button """
        if self.interface.LEFT_KEY and not self.draw_button.active:     # If they pressed left or right
            if self.cursor_rect.x == self.image_list[0].x:  # If they press left while on the 1st card
                self.cursor_rect.x = self.image_list[-1].x   # Move cursor to the last card
            else:  # If the cursor is not on the left-most image
                self.cursor_rect.x -= 90    # Moves the cursor rectangle

        elif self.interface.RIGHT_KEY and not self.draw_button.active:
            if self.cursor_rect.x == self.image_list[-1].x:  # If the cursor is on the left-most card
                self.cursor_rect.x = self.image_list[0].x   # Move it onto the 1st card
            else:
                self.cursor_rect.x += 90

        elif self.interface.UP_KEY and not self.draw_button.active:
            self.draw_button.colour = self.draw_button.colour_active
            self.draw_button.active = True
            self.cursor_rect.y += 1000  # Move it out of the screen

        elif self.interface.DOWN_KEY and self.draw_button.active:
            self.cursor_rect.y -= 1000  # Bring it back onto screen
            self.draw_button.active = False
            self.draw_button.colour = self.draw_button.colour_passive

    def check_input(self):
        """ Checks if they have pressed a key and performs the necessary actions """
        self.move_cursor()

        if self.interface.ENTER_KEY and not self.draw_button.active:
            for image in self.image_list:
                if self.cursor_rect.x == image.x:   # If the cursor overlaps with the image's rectangle
                    card_index = self.image_list.index(image)   # The pos of the chosen card in the image list and deck
                    self.choose_card(card_index)    # Uses the index to check if that card in the deck is valid

                    if self.interface.card_chosen:
                        self.invalid = False
                        self.deck.pop(card_index)   # So the card doesn't get displayed among your deck

        elif self.interface.ENTER_KEY and self.draw_button.active:
            self.action = DrawCard()    # To tell the server after that the player wants to draw a card
            self.interface.card_chosen = True   # Stops the loop in the client

            self.draw_button.active = False     # Resetting it
            self.draw_button.colour = self.draw_button.colour_passive
            self.cursor_rect.y -= 1000


    def ask(self, game):
        """ Asks the user if they want to place their drawn card down """
        self.interface.screen.fill((0, 100, 255))
        self.interface.check_events()

        ask_text = self.button_font.render("Place The Card Down?", True, (255, 255, 255))
        self.interface.screen.blit(ask_text, (self.MID_W - ask_text.get_width() / 2, self.MID_H - 400))

        your_player = game.player_list[self.player_id]
        picked_up_card = self.scale_image(your_player.deck[-1])   # The card you just picked up is at index -1
        self.interface.screen.blit(picked_up_card, (self.MID_W - picked_up_card.get_width() / 2, self.MID_H - 200))
        # display the picked up card, add text for choosing colour, create new colour cursor

        self.interface.screen.blit(self.yes_text, (self.MID_W + 215,    # Drawing the text and buttons onto screen
                                                   self.MID_H + 125))
        self.interface.screen.blit(self.no_text, (self.MID_W - 275,
                                                  self.MID_H + 125))
        self.yes_button.draw_rect(self.interface.screen)
        self.no_button.draw_rect(self.interface.screen)

        if self.interface.LEFT_KEY:     # Moves the cursor rect so you can select an option
            if self.ask_cursor.rect.x != self.no_button.rect.x:  # If it's not already on the no button
                self.ask_cursor.rect.x -= 500
        elif self.interface.RIGHT_KEY:
            if self.ask_cursor.rect.x != self.yes_button.rect.x:
                self.ask_cursor.rect.x += 500

        elif self.interface.ENTER_KEY:
            if self.ask_cursor.rect.x == self.yes_button.rect.x:
                self.action = Decision("Yes")
            else:
                self.action = Decision("No")

            self.confirm = False    # To stop the loop in the client

        self.ask_cursor.draw_rect(self.interface.screen)
        pygame.display.update()
        self.interface.clock.tick(60)
        self.reset_keys()

    def choose_colour(self):
        self.interface.screen.fill((pygame.Color("cornflowerblue")))
        self.interface.check_events()
        font = pygame.font.Font(None, 80)

        choose_text = font.render("Choose A Colour", True, (255, 255, 255))
        self.interface.screen.blit(choose_text, (self.MID_W - choose_text.get_width() / 2, self.MID_H - 300))

        # Create an image object for each diamond and assign their images and co-ordinates to attributes
        red_diamond = Image(pygame.transform.scale(self.red_d, (self.red_d.get_width() * 0.6,
                                                                self.red_d.get_height() * 0.6)), colour="red")
        diamond_width = red_diamond.image.get_width()
        red_diamond.x, red_diamond.y = self.MID_W - (75 + diamond_width * 2), self.MID_H - diamond_width / 2

        blue_diamond = Image(pygame.transform.scale(self.blue_d, (self.blue_d.get_width() * 0.6,
                                                                  self.blue_d.get_height() * 0.6)), colour="blue")
        blue_diamond.x, blue_diamond.y = self.MID_W - (25 + diamond_width), self.MID_H - diamond_width / 2

        green_diamond = Image(pygame.transform.scale(self.green_d, (self.green_d.get_width() * 0.6,
                                                                    self.green_d.get_height() * 0.6)), colour="green")
        green_diamond.x, green_diamond.y = self.MID_W + 25, self.MID_H - diamond_width / 2

        yellow_diamond = Image(pygame.transform.scale(self.yellow_d, (self.yellow_d.get_width() * 0.6,
                                                                      self.yellow_d.get_height() * 0.6)), colour="yellow")
        yellow_diamond.x, yellow_diamond.y = self.MID_W + 75 + diamond_width, self.MID_H - diamond_width / 2

        diamond_list = [red_diamond, blue_diamond, green_diamond, yellow_diamond]

        for diamond in diamond_list:    # Blit all 4 diamonds
            self.interface.screen.blit(diamond.image, (diamond.x, diamond.y))

        if not self.colour_cursor: # If hasn't been drawn yet - stops the cursor from being drawn at initial position
            self.colour_cursor = red_diamond.image.get_rect(topleft=(self.MID_W - (75 + diamond_width * 2),
                                                                     self.MID_H - diamond_width / 2))

        if self.interface.LEFT_KEY:
            if self.colour_cursor.x == diamond_list[0].x:   # If the cursor is at the first card (leftmost)
                self.colour_cursor.x = diamond_list[-1].x   # Move cursor from the left side to the right
            else:
                self.colour_cursor.x -= (50 + diamond_width)

        elif self.interface.RIGHT_KEY:
            if self.colour_cursor.x == diamond_list[-1].x:
                self.colour_cursor.x = diamond_list[0].x    # Move cursor from the right side to the left
            else:
                self.colour_cursor.x += (50 + diamond_width)

        elif self.interface.ENTER_KEY:  # If they selected a colour
            for diamond in diamond_list:
                if self.colour_cursor.x == diamond.x:     # Find the selected colour
                    self.new_colour = diamond.colour
                    self.choosing_colour = False

        pygame.draw.rect(self.interface.screen, pygame.Color("gray25"), self.colour_cursor, 3)

        self.interface.clock.tick(60)
        self.reset_keys()
        pygame.display.update()
















