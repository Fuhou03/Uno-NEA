class Response:
    def __init__(self, game, payload):
        self.game = game    # the new game state
        self.payload = payload      # payload -  might be None - this is for additional data


class PlaceCard:
    def __init__(self, p_id, choice, **kw):
        self.p_id = p_id
        self.choice = choice    # A number representing the player's choice
        self.colour = kw.get("colour")

    def execute(self, game):
        current_player = game.player_list[game.turn]    # Changes every turn

        if self.p_id == current_player.id:
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

        else:
            return Response(game, None)     # No changes    (might need to change this)


class DrawCard:
    def __init__(self, p_id):
        self.p_id = p_id

    def execute(self, game):
        current_player = game.player_list[game.turn]

        if self.p_id == current_player.id:
            current_player.deck = game.dk.draw_card(current_player.deck)  # Draw 1 card from main deck

            # If the card you drew is valid you can place it down immediately
            if current_player.deck[-1].colour == game.discard_pile[-1].colour or \
                    current_player.deck[-1].value == game.discard_pile[-1].value:

                #ask = input(f"The {current_player.deck[-1].colour} - {current_player.deck[-1].value}"
                            #f" card you picked up is valid, do you want to place it down? Type 'y' or 'n': ")

                #if ask == "y":
                game.discard_pile.append(current_player.deck[-1])
                current_player.deck.pop(-1)

                return Response(game, "executed")
                #else:   # They don't place the card down
                    #return Response(game, "drawn")
                    #self.move_on = True

            else:   # If they card they drew cannot be placed down, it moves on
                game.turn = game.next_turn()
                return Response(game, None)
                #self.move_on = True

        else:
            return Response(game, None)     # No changes    (might need to change this)


