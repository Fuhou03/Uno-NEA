from player import Player
from deck import Deck

class Uno:
    def __init__(self):
        self.connected = 0
        self.direction = "clockwise"
        self.turn = 0  # My turn is 0, P2 is 1

        self.started = False
        self.finished = False

        self.player_list = []    # Create the players
        self.discard_pile = []

        #self.current_player = None

        self.dk = Deck()


    """def two_player():
        dk = Deck()
        dk.create_deck()
        dk.shuffle()
    
        ai = Player()
        ai.deck = dk.deal_cards(ai.deck)
    
        me = Player()
        me.deck = dk.deal_cards(me.deck)
    
        discard_pile = []
        discard_pile.append(dk.deck[0])  # Card at the top of the deck is placed down first
    
        turn = 1  # My turn (2 is the AI's turn)
        finished = False
        while not finished:
            if turn == 1:
                display_pile(discard_pile)
                display_deck(me.deck, 1)
    
                discard_pile, dk = me.choose_card(discard_pile, dk)
    
                if me.drew_card == True:
                    turn = 2  # Moves onto opponent after I drew a card
    
                elif discard_pile[-1].value == "skip" or discard_pile[-1] == "reverse":
                    turn = 1  # So the opponent's turn is skipped
                    print("The opponent's turn is skipped")
    
                elif discard_pile[-1].value == "wild 4":
                    print("The opponent's turn is skipped \n")
                    for i in range(4):
                        ai.deck = dk.draw_card(ai.deck)
                    turn = 1
    
                elif discard_pile[-1].value == "draw 2":
                    for i in range(2):
                        ai.deck = dk.draw_card(ai.deck)
    
                else:
                    turn = 2
    
    
    
            else:
                display_deck(ai.deck, 2)
                display_pile(discard_pile)
                print("\nIt is the opponent's turn. \nThey have performed an action. \n")
    
                discard_pile, dk = ai.select_card(discard_pile, dk)
    
                if discard_pile[-1].value == "wild 4":
                    turn = 2  # My turn is skipped and I draw 4 cards
                    for i in range(4):
                        me.deck = dk.draw_card(me.deck)
                        print("Your turn is skipped")
    
                elif discard_pile[-1].value == "draw 2":
                    for i in range(2):
                        me.deck = dk.draw_card(me.deck)
                    turn = 2
                    print("Your turn is skipped")
    
                elif discard_pile[-1].value == "skip" or discard_pile[-1].value == "reverse":
                    turn = 2
                    print("Your turn is skipped")
    
                else:
                    turn = 1  # My turn
    
            if len(me.deck) == 0:
                finished = True
                print("You won!")
            elif len(ai.deck) == 0:
                print("You lost!")
            elif len(ai.deck) == 1:
                print("Your opponent said: 'UNO!'") """


    def display_info(self):
        current_player = self.player_list[self.turn]    # Changes every turn

        print(f"\nThe current direction: {self.direction}")

        print(f"The card at the top of the Discard pile:"
              f" {self.discard_pile[-1].colour} - {self.discard_pile[-1].value}\n")

        print("Your deck is:")

        for i in range(0, len(current_player.deck)):
            print(f"{i}: {current_player.deck[i].colour} - {current_player.deck[i].value}")


    def change_direction(self):
        if self.direction == "clockwise":
            self.direction = "anticlockwise"
        else:
            self.direction = "clockwise"


    def next_turn(self):
        """ Increments or decrements the turn variable to determine whose turn is next """
        if self.direction == "clockwise":
            self.turn = (self.turn + 1) % 3   # Becomes 0 if it reaches 3, becomes 1 if it's 4 etc. to stop index errors
        else:
            self.turn -= 1
            if self.turn == -1:   # Prevents index errors
                self.turn = 2    # So it goes back to the AI (turn 2) after P1 has their turn (0)
        return self.turn


        '''elif player.id == 2:   # Program selects the card for P3 (AI)
            colours = ["red", "blue", "yellow", "green"]
            random.shuffle(player..deck)

            for i in range(0, len(player.deck)):  # Select the first matching card and remove it from their hand
                current_card = player.deck[i]

                if (current_card.colour == self.discard_pile[-1].colour) or\
                        (current_card.value == self.discard_pile[-1].value):
                    # If the current card matches with the card at the top of the discard pile
                    self.discard_pile.append(current_card)
                    player.deck.pop(i)
                    return self.discard_pile

                elif current_card.value == "wild" or current_card.value == "wild 4":  # If a wild card is chosen
                    random_colour = random.choice(colours)  # Select a random colour for the next player
                    current_card.colour = random_colour     # "None" property turns into the selected colour
                    self.discard_pile.append(current_card)

                    print(f"A wildcard was selected and the colour chosen is {random_colour}")

                    player.deck.pop(i)
                    return self.discard_pile

            return self.discard_pile     # No matching card found'''

    def compare_card(self):
        next_player = self.player_list[self.next_turn()] # next_turn called so the index's incremented/decremented
        current_player = self.player_list[self.turn]    # Changes every turn

        if len(current_player.deck) == 1:
            print(f"Player {current_player.id} said UNO!")

        if self.discard_pile[-1].value == "draw 2":
            # Next player draws 2 and their turn is skipped
            for i in range(2):
                next_player.deck = self.dk.draw_card(next_player.deck)

            print(f"Player {next_player.id}'s turn is skipped.")

            for i in range(2): # Turn increments twice so it skips the next player
                self.turn = self.next_turn()

        elif self.discard_pile[-1].value == "skip":
            print(f"Player {next_player.id}'s turn is skipped.")

            for i in range(2):
                self.turn = self.next_turn()

        elif self.discard_pile[-1].value == "reverse":
            print(f"\nPlayer {next_player.id}'s turn is skipped.") # Printed before the reverse
            self.change_direction()
            self.turn = self.next_turn()

        elif self.discard_pile[-1].value == "wild 4":
            for i in range(4):  # Next player draws 4 cards
                next_player.deck = self.dk.draw_card(next_player.deck)

            print(f"Player {next_player.id}'s turn is skipped.")

            for i in range(2):
                self.turn = self.next_turn()

        else:  # Normal numbered card placed down
            self.turn = self.next_turn()

        if len(current_player.deck) == 0:
            print(f"Player {current_player.id} has won! The game has completed.")
            self.finished = True


    def set_up(self):
        """ Give each player 7 cards and add the card at the top of the deck to the discard pile """
        self.dk.create_deck()
        self.dk.shuffle()
        self.player_list = [Player(0), Player(1), Player(2)]

        for player in self.player_list:
            player.deck = self.dk.deal_cards(player.deck)    # Give the players 7 cards

        for i in range(0, len(self.dk.deck)): # So the game doesn't start with a wild card
            if self.dk.deck[i].colour != "None":
                self.discard_pile.append(self.dk.deck[i]) # Card at the top of the deck is placed down first (index 0)
                break

        #self.discard_pile_length = len(self.discard_pile)


    def play_game(self, game_mode):

        while True:
            print("\n", end="")

            if game_mode == 2:
                pass
                #self.two_player()
                #break
            elif game_mode == 3:
                self.set_up()
                break




