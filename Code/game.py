from deck import Deck

class Player:
    def __init__(self, id):
        self.deck = []
        self.id = id


class Uno:
    def __init__(self):
        self.direction = "clockwise"
        self.turn = 0

        self.game_mode = None
        self.finished = False

        self.player_list = []
        self.discard_pile = []

        self.dk = Deck()

    def add_player(self, player_id):
        self.player_list.append(Player(player_id))    # Create new player

    def change_direction(self):
        if self.direction == "clockwise":
            self.direction = "anticlockwise"
        else:
            self.direction = "clockwise"

    def next_turn(self):
        """ Increments or decrements the turn variable to determine whose turn is next """
        # A separate variable so I can use next_turn as an index to find the next player
        # Or else self.turn would be incremented every time I call this method
        next_turn = self.turn

        if self.direction == "clockwise":
            next_turn = (self.turn + 1) % len(self.player_list)     # Becomes 0 if it reaches 3, to stop index errors
        else:
            next_turn -= 1
            if next_turn == -1:   # Prevents index errors
                next_turn = len(self.player_list) - 1    # E.g. so it goes back to P2 after P0 has their turn

        return next_turn

    def compare_card(self):
        # self.player_list[self.next_turn()] is the next player

        if self.discard_pile[-1].value == "draw 2":
            # Next player draws 2 and their turn is skipped
            for i in range(2):  # next_turn is called so you get the index of the next player
                self.player_list[self.next_turn()].deck = self.dk.draw_card(self.player_list[self.next_turn()].deck)

            #print(f"Player {self.player_list[self.next_turn()].id}'s turn is skipped.")

            for i in range(2): # Turn increments twice so it skips the next player
                self.turn = self.next_turn()

        elif self.discard_pile[-1].value == "skip":
            #print(f"Player {self.player_list[self.next_turn()].id}'s turn is skipped.")

            for i in range(2):
                self.turn = self.next_turn()

        elif self.discard_pile[-1].value == "reverse":
            #print(f"\nPlayer {self.player_list[self.next_turn()].id}'s turn is skipped.") # Printed before the reverse
            self.change_direction()
            self.turn = self.next_turn()

            if self.game_mode == 2:     # Reverse acts as a skip card in 2 player mode
                self.turn = self.next_turn()    # Returns back to you

        elif self.discard_pile[-1].value == "wild 4":
            for i in range(4):  # Next player draws 4 cards
                self.player_list[self.next_turn()].deck = self.dk.draw_card(self.player_list[self.next_turn()].deck)

            #print(f"Player {self.player_list[self.next_turn()].id}'s turn is skipped.")

            for i in range(2):
                self.turn = self.next_turn()

        else:  # Normal numbered card placed down
            self.turn = self.next_turn()

        if len(self.player_list[self.turn].deck) == 0:
            self.finished = True

    def set_up(self):
        """ Give each player 7 cards and add the card at the top of the deck to the discard pile """
        self.dk.create_deck()
        self.dk.shuffle()

        for player in self.player_list:
            player.deck = self.dk.deal_cards(player.deck)    # Give the players 7 cards

        for i in range(0, len(self.dk.deck)): # So the game doesn't start with a wild card
            if self.dk.deck[i].colour != None:
                self.discard_pile.append(self.dk.deck[i]) # Card at the top of the deck is placed down first (index 0)
                break

    def start_game(self, game_mode):
        self.game_mode = game_mode
        self.set_up()





