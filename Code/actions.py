class Response:
    def __init__(self, game, payload):
        self.game = game    # the new game state
        self.payload = payload      # payload -  might be None - this is for additional data


class PlaceCard:    # Used to tell the server which card you want to place down
    def __init__(self, choice, **kw):
        self.choice = choice    # A number representing the player's choice
        self.colour = kw.get("colour")
        self.pressed_uno = None

    def execute(self, game):    # The server calls this method once it receives the object
        # Checks the colour of the card that the player just picked. A wildcard would have no colour.
        if game.player_list[game.turn].deck[self.choice].colour is None:      # If they chose a wild card
            # Replaces the wild card's 'None' colour with the colour chosen and places that card down
            game.player_list[game.turn].deck[self.choice].colour = self.colour

        # If it's not a wild card then it simply places the card down
        game.discard_pile.append(game.player_list[game.turn].deck[self.choice])     # Add the card to the discard pile
        game.player_list[game.turn].deck.pop(self.choice)       # Remove it from your deck

        if len(game.player_list[game.turn].deck) == 1 and self.pressed_uno is True:  # 1 card remaining and they pressed the uno button already
            game.pressed_uno = [game.turn, True]    # Use a list so we know which player pressed Uno
        else:
            game.pressed_uno = None

        return Response(game, "Executed")


class DrawCard:     # This is sent to the server to tell them that you want to draw a card
    def __init__(self):
        pass

    def execute(self, game):
        # The draw card method from the Deck object inside the game object is called. Current P's deck is the parameter
        game.player_list[game.turn].deck = game.dk.draw_card(game.player_list[game.turn].deck)  # Draw 1 card

        if game.pressed_uno is not None:    # If the previous player pressed the Uno button
            game.pressed_uno = None     # Reset it

        # If the card you drew is valid the player will be asked if they want to place it down immediately -
        if game.player_list[game.turn].deck[-1].colour == game.discard_pile[-1].colour or \
                game.player_list[game.turn].deck[-1].value == game.discard_pile[-1].value:
            return Response(game, "Confirm")

        else:   # If the card they drew cannot be placed down, it increments the turn so the game moves on
            game.turn = game.next_turn()
            return Response(game, None)


class Decision:     # This is sent to the server to tell them whether to place the picked up card down, or not
    def __init__(self, decision):
        self.decision = decision

    def execute(self, game):
        if self.decision == "Yes":    # If they chose to place down the card that they picked up
            game.discard_pile.append(game.player_list[game.turn].deck[-1])
            game.player_list[game.turn].deck.pop(-1)
            return Response(game, "Executed")

        else:   # Moves onto the next player without placing the card down
            game.turn = game.next_turn()
            return Response(game, None)



