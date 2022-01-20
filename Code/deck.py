from card import Card
import random


class Deck:
    def __init__(self):
        self.colours = ["red", "blue", "yellow", "green"]
        self.deck = []

    def create_deck(self):
        for i in range(0, 2):  # Each num has 2 cards for each colour so 8 in total
            for num in range(0, 10):  # Create cards 0-9.
                for colour in self.colours:
                    self.deck.append(Card(colour, num))

            for colour in self.colours:  # For special cards. 2 special cards for each colour (8 in total)
                # e.g 2 red skips, 2 red reverse, 2 red draw2
                self.deck.append(Card(colour, "skip"))
                self.deck.append(Card(colour, "reverse"))
                self.deck.append(Card(colour, "draw 2"))

        for i in range(4):
            self.deck.append(Card(None, "wild 4"))
            self.deck.append(Card(None, "wild"))  # Changes colour only

    def shuffle(self):  # Make my own shuffle method later
        for i in range(5):
            random.shuffle(self.deck)

    def deal_cards(self, player_deck):
        ''' Deal 7 cards to the player and remove the 7 cards from the main deck'''

        for i in range(7):
            player_deck.append(self.deck[0])
            self.deck.pop(0)  # Remove from the back of the deck

        return player_deck

    def draw_card(self, player_deck):
        """ When player chooses to draw a card """
        player_deck.append(self.deck[0])
        self.deck.pop(0)

        return player_deck
