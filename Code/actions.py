class Response:
    def __init__(self, game, payload):
        self.game = game    # the new game state
        self.payload = payload      # payload -  might be None - this is for additional data

class PlaceCard:
    def __init__(self, decision):
        self.decision = decision

    def execute(self, game):
        if self.decision == "y":
            game.discard_pile.append(current_player.deck[-1])
            game.current_player.deck.pop(-1)
            return Response(game, "executed")
        else:
            return Response(game, None)

class CheckCard:
    def __init__(self, choice, **kw):
        self.choice = choice    # A number representing the player's choice
        self.colour = kw.get("colour")

    def execute(self, game):
        current_player = game.player_list[game.turn]    # Changes every turn

        # If my choice matches correctly
        if (current_player.deck[self.choice].colour == game.discard_pile[-1].colour) or \
                (current_player.deck[self.choice].value == game.discard_pile[-1].value):
            game.discard_pile.append(current_player.deck[self.choice])  # Add the card to the discard pile

            current_player.deck.pop(self.choice)  # Remove it from your deck
            return Response(game, "executed")

        elif current_player.deck[self.choice].value == "wild" or\
                current_player.deck[self.choice].value == "wild 4":
            # If they chose a wild card - the colour of the card at the top of the pile changes
            current_player.deck[self.choice].colour = self.colour
            game.discard_pile.append(current_player.deck[self.choice])

            current_player.deck.pop(self.choice)
            return Response(game, "executed")



class DrawCard:
    def __init__(self):
        pass

    def execute(self, game):
        current_player = game.player_list[game.turn]

        current_player.deck = game.dk.draw_card(current_player.deck)  # Draw 1 card from main deck

        # If the card you drew is valid you can place it down immediately
        if current_player.deck[-1].colour == game.discard_pile[-1].colour or \
                current_player.deck[-1].value == game.discard_pile[-1].value:
            return Response(game, "confirm")

        else:   # If they card they drew cannot be placed down, it moves on
            game.turn = game.next_turn()
            return Response(game, None)
            #self.move_on = True



