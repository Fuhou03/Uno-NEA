class Response:
    def __init__(self, game, payload):
        self.game = game    # the new game state
        self.payload = payload      # payload -  might be None - this is for additional data


class Decision:
    def __init__(self, decision):
        self.decision = decision

    def execute(self, game):
        if self.decision == "y":    # If they chose to place down the card that they picked up
            game.discard_pile.append(game.player_list[game.turn].deck[-1])
            game.player_list[game.turn].deck.pop(-1)
            return Response(game, "Executed")

        else:   # Moves onto the next player without placing the card down
            game.turn = game.next_turn()
            return Response(game, None)


class PlaceCard:
    def __init__(self, choice, **kw):
        self.choice = choice    # A number representing the player's choice
        self.colour = kw.get("colour")

    def execute(self, game):
        #if (game.player_list[game.turn].deck[self.choice].colour == game.discard_pile[-1].colour) or \
        #        (game.player_list[game.turn].deck[self.choice].value == game.discard_pile[-1].value):
        #
        #    game.discard_pile.append(game.player_list[game.turn].deck[self.choice])
        #    game.player_list[game.turn].deck.pop(self.choice)
        #    return Response(game, "Executed")

        if game.player_list[game.turn].deck[self.choice].colour == None:      # If they chose a wild card
            # Replaces the wild card's 'None' colour with the colour chosen and places that card down
            game.player_list[game.turn].deck[self.choice].colour = self.colour

        game.discard_pile.append(game.player_list[game.turn].deck[self.choice])     # Add the card to the discard pile
        game.player_list[game.turn].deck.pop(self.choice)       # Remove it from your deck

        return Response(game, "Executed")


class DrawCard:
    def __init__(self):
        self.temp = None

    def execute(self, game):
        # The draw card method from the Deck object inside the game object is called
        game.player_list[game.turn].deck = game.dk.draw_card(game.player_list[game.turn].deck)  # Draw 1 card

        # If the card you drew is valid it asks the user if they want to place it down immediately -
        if game.player_list[game.turn].deck[-1].colour == game.discard_pile[-1].colour or \
                game.player_list[game.turn].deck[-1].value == game.discard_pile[-1].value:
            return Response(game, "confirm")

        else:   # If they card they drew cannot be placed down, it increments the turn so the game moves on
            game.turn = game.next_turn()
            return Response(game, None)



