import random

class Card:
    def __init__(self, colour, value, **kwargs):
        self.colour = colour
        self.value = value
        self.image = kwargs.get("image")

class Deck:
    def __init__(self):
        self.colours = ["red", "blue", "green", "yellow"]
        self.deck = []
        self.images = Images()

    def create_deck(self):
        colour_index = 0    # Used to get the image from the correct list inside the 2D card_list

        for i in range(0, 2):   # Each number has 2 cards for each colour (e.g Two blue-8s in a deck)
            for num in range(0,13):     # Creates the cards for every colour
                for colour in self.colours:
                    # 2 special cards of each type for every colour e.g 2 red skips, 2 red reverse, 2 red draw_2
                    if num == 10:
                        self.deck.append(Card(colour, "draw 2", image=self.images.card_list[colour_index][num]))
                    elif num == 11:
                        self.deck.append(Card(colour, "reverse", image=self.images.card_list[colour_index][num]))
                    elif num == 12:
                        self.deck.append(Card(colour, "skip", image=self.images.card_list[colour_index][num]))
                    else:   # Creating the card objects and adding them to the deck
                        self.deck.append(Card(colour, num, image=self.images.card_list[colour_index][num]))
                    colour_index += 1   # Incremented so it moves onto the next colour in card_list
                colour_index = 0    # Reset to 0 to select from the red_cards list again

        for i in range(4):  # 4 wild cards and 4 wild 4 cards in a deck
            self.deck.append(Card(None, "wild 4", image=self.images.wild_4))
            self.deck.append(Card(None, "wild", image=self.images.wild))  # Changes colour only

    def shuffle(self):  # Make my own shuffle method later
        for i in range(5):
            random.shuffle(self.deck)

    def deal_cards(self, player_deck):
        ''' Deal 7 cards to the player and remove the 7 cards from the main deck'''

        for i in range(7):
            player_deck.append(self.deck[0])
            self.deck.pop(0)  # Remove from the back of the deck

        return player_deck


class Images:
    def __init__(self):
        #self.red_0 = pygame.image.load("Uno Cards\Red 0.png").convert_alpha()  # Load image later
        self.red_0 = ("Uno Cards\Red 0.png")    # Can get rid of these variables probably
        self.red_1 = ("Uno Cards\Red 1.png")
        self.red_2 = ("Uno Cards\Red 2.png")
        self.red_3 = ("Uno Cards\Red 3.png")
        self.red_4 = ("Uno Cards\Red 4.png")
        self.red_5 = ("Uno Cards\Red 5.png")
        self.red_6 = ("Uno Cards\Red 6.png")
        self.red_7 = ("Uno Cards\Red 7.png")
        self.red_8 = ("Uno Cards\Red 8.png")
        self.red_9 = ("Uno Cards\Red 9.png")

        self.red_draw_2 = ("Uno Cards\Red Draw 2.png")
        self.red_reverse = ("Uno Cards\Red Reverse.png")
        self.red_skip = ("Uno Cards\Red Skip.png")

        self.blue_0 = ("Uno Cards\Blue 0.png")
        self.blue_1 = ("Uno Cards\Blue 1.png")
        self.blue_2 = ("Uno Cards\Blue 2.png")
        self.blue_3 = ("Uno Cards\Blue 3.png")
        self.blue_4 = ("Uno Cards\Blue 4.png")
        self.blue_5 = ("Uno Cards\Blue 5.png")
        self.blue_6 = ("Uno Cards\Blue 6.png")
        self.blue_7 = ("Uno Cards\Blue 7.png")
        self.blue_8 = ("Uno Cards\Blue 8.png")
        self.blue_9 = ("Uno Cards\Blue 9.png")

        self.blue_draw_2 = ("Uno Cards\Blue Draw 2.png")
        self.blue_reverse = ("Uno Cards\Blue Reverse.png")
        self.blue_skip = ("Uno Cards\Blue Skip.png")

        self.green_0 = ("Uno Cards\Green 0.png")
        self.green_1 = ("Uno Cards\Green 1.png")
        self.green_2 = ("Uno Cards\Green 2.png")
        self.green_3 = ("Uno Cards\Green 3.png")
        self.green_4 = ("Uno Cards\Green 4.png")
        self.green_5 = ("Uno Cards\Green 5.png")
        self.green_6 = ("Uno Cards\Green 6.png")
        self.green_7 = ("Uno Cards\Green 7.png")
        self.green_8 = ("Uno Cards\Green 8.png")
        self.green_9 = ("Uno Cards\Green 9.png")

        self.green_draw_2 = ("Uno Cards\Green Draw 2.png")
        self.green_reverse = ("Uno Cards\Green Reverse.png")
        self.green_skip = ("Uno Cards\Green Skip.png")

        self.yellow_0 = ("Uno Cards\Yellow 0.png")
        self.yellow_1 = ("Uno Cards\Yellow 1.png")
        self.yellow_2 = ("Uno Cards\Yellow 2.png")
        self.yellow_3 = ("Uno Cards\Yellow 3.png")
        self.yellow_4 = ("Uno Cards\Yellow 4.png")
        self.yellow_5 = ("Uno Cards\Yellow 5.png")
        self.yellow_6 = ("Uno Cards\Yellow 6.png")
        self.yellow_7 = ("Uno Cards\Yellow 7.png")
        self.yellow_8 = ("Uno Cards\Yellow 8.png")
        self.yellow_9 = ("Uno Cards\Yellow 9.png")

        self.yellow_draw_2 = ("Uno Cards\Yellow Draw 2.png")
        self.yellow_reverse = ("Uno Cards\Yellow Reverse.png")
        self.yellow_skip = ("Uno Cards\Yellow Skip.png")

        self.wild = ("Uno Cards\Wild.png")
        self.wild_4 = ("Uno Cards\Wild 4.png")
        self.card_back = ("Uno Cards\Back Of Card.png")

        self.red_diamond = ("Uno Cards\Red Diamond.png")
        self.blue_diamond = ("Uno Cards\Blue Diamond.png")
        self.green_diamond = ("Uno Cards\Green Diamond.png")
        self.yellow_diamond = ("Uno Cards\Yellow Diamond.png")

        self.clockwise = ("Uno Cards\Clockwise.png")
        self.anticlockwise = ("Uno Cards\Anticlockwise.png")

        self.card_list = []
        self.red_cards = []
        self.green_cards = []
        self.blue_cards = []
        self.yellow_cards = []

        self.create_card_list()

    def create_card_list(self):
        """ Add the images into separate lists then combine them to create a 2D List """
        self.red_cards.append(self.red_0)
        self.red_cards.append(self.red_1)
        self.red_cards.append(self.red_2)
        self.red_cards.append(self.red_3)
        self.red_cards.append(self.red_4)
        self.red_cards.append(self.red_5)
        self.red_cards.append(self.red_6)
        self.red_cards.append(self.red_7)
        self.red_cards.append(self.red_8)
        self.red_cards.append(self.red_9)
        self.red_cards.append(self.red_draw_2)
        self.red_cards.append(self.red_reverse)
        self.red_cards.append(self.red_skip)

        self.blue_cards.append(self.blue_0)
        self.blue_cards.append(self.blue_1)
        self.blue_cards.append(self.blue_2)
        self.blue_cards.append(self.blue_3)
        self.blue_cards.append(self.blue_4)
        self.blue_cards.append(self.blue_5)
        self.blue_cards.append(self.blue_6)
        self.blue_cards.append(self.blue_7)
        self.blue_cards.append(self.blue_8)
        self.blue_cards.append(self.blue_9)
        self.blue_cards.append(self.blue_draw_2)
        self.blue_cards.append(self.blue_reverse)
        self.blue_cards.append(self.blue_skip)

        self.green_cards.append(self.green_0)
        self.green_cards.append(self.green_1)
        self.green_cards.append(self.green_2)
        self.green_cards.append(self.green_3)
        self.green_cards.append(self.green_4)
        self.green_cards.append(self.green_5)
        self.green_cards.append(self.green_6)
        self.green_cards.append(self.green_7)
        self.green_cards.append(self.green_8)
        self.green_cards.append(self.green_9)
        self.green_cards.append(self.green_draw_2)
        self.green_cards.append(self.green_reverse)
        self.green_cards.append(self.green_skip)

        self.yellow_cards.append(self.yellow_0)
        self.yellow_cards.append(self.yellow_1)
        self.yellow_cards.append(self.yellow_2)
        self.yellow_cards.append(self.yellow_3)
        self.yellow_cards.append(self.yellow_4)
        self.yellow_cards.append(self.yellow_5)
        self.yellow_cards.append(self.yellow_6)
        self.yellow_cards.append(self.yellow_7)
        self.yellow_cards.append(self.yellow_8)
        self.yellow_cards.append(self.yellow_9)
        self.yellow_cards.append(self.yellow_draw_2)
        self.yellow_cards.append(self.yellow_reverse)
        self.yellow_cards.append(self.yellow_skip)

        self.card_list.append(self.red_cards)   # Create 2D list
        self.card_list.append(self.blue_cards)
        self.card_list.append(self.green_cards)
        self.card_list.append(self.yellow_cards)

        self.card_list.append(self.wild)
        self.card_list.append(self.wild_4)
