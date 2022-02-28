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
        self.winner = None
        self.finished = False

        self.pressed_uno = False    # This is assigned the ID of the player that pressed the Uno button later
        self.forgot_player = False  # This is assigned the ID of the player that forgot to press Uno

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

    def draw_card(self, player_deck):
        """ When player chooses to draw a card """
        player_deck.append(self.dk.deck[0])
        self.dk.deck.pop(0)


    def compare_card(self):
        # self.player_list[self.next_turn()] is the next player
        current_turn = self.turn    # Used to check if the player has placed the final card down (as self.turn changes)

        if self.discard_pile[-1].value == "draw 2":
            # Next player draws 2 and their turn is skipped
            for i in range(2):  # next_turn is called so you get the index of the next player
                self.draw_card(self.player_list[self.next_turn()].deck)

            for i in range(2): # Turn increments twice so it skips the next player
                self.turn = self.next_turn()

        elif self.discard_pile[-1].value == "skip":
            for i in range(2):
                self.turn = self.next_turn()

        elif self.discard_pile[-1].value == "reverse":
            self.change_direction()
            self.turn = self.next_turn()

            if self.game_mode == 2:     # Reverse acts as a skip card in 2 player mode
                self.turn = self.next_turn()    # Returns back to you

        elif self.discard_pile[-1].value == "wild 4":
            for i in range(4):  # Next player draws 4 cards
                self.draw_card(self.player_list[self.next_turn()].deck)
            
            for i in range(2):
                self.turn = self.next_turn()

        else:  # Normal numbered card placed down
            self.turn = self.next_turn()

        if len(self.player_list[current_turn].deck) == 0:  # If a player has placed all their cards down
            self.finished = True
            self.winner = current_turn
        elif len(self.player_list[current_turn].deck) == 1:     # If they have 1 card remaining
            self.check_for_uno()

    def check_for_uno(self):
        """ Checks if the player remembered to say Uno before putting down his 2nd to last card """

        if self.forgot_player is not False:     # They forgot
            for i in range(4):  # They must draw 4 cards
                self.draw_card(self.player_list[self.forgot_player].deck)


    def set_up(self):
        """ Give each player 7 cards and add the card at the top of the deck to the discard pile """
        self.dk.create_deck()
        self.dk.shuffle()

        for player in self.player_list:
            player.deck = self.dk.deal_cards(player.deck)    # Give the players 7 cards

        for i in range(0, len(self.dk.deck)): # So the game doesn't start with a wild card
            if self.dk.deck[i].colour is not None:
                self.discard_pile.append(self.dk.deck[i]) # Card at the top of the deck is placed down first (index 0)
                break

    def start_game(self, game_mode):
        self.game_mode = game_mode
        self.set_up()





