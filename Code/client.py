from network import Network
from actions import PlaceCard, DrawCard

def choose_card(player_id, game):
    """ To choose your own card """

    current_player = game.player_list[game.turn]

    valid = False
    while not valid:
        try:
            choice = int(input("\nChoose a card by typing it's number at the front. \n"
                               "If you have no valid cards then type any string to draw a card: "))
            print("")
            if choice >= len(current_player.deck) or choice < 0:  # If they enter an invalid number
                raise IndexError

        except ValueError:  # If they entered a string
            #self.drew_card = True   # To call the function again after
            #self.draw_card()
            return DrawCard(player_id)

        except IndexError:
            print("That card is not possible. Please enter the number correctly. \n")
            continue    # They will have to enter again

        else:
            if current_player.deck[choice].colour == "None":   # wildcard
                new_colour = input("Choose a colour for the next player: ")
                return PlaceCard(player_id, choice, colour=new_colour)  # Colour an optional parameter

            #elif (current_player.deck[choice].colour != game.discard_pile[-1].colour) or \
                    #(current_player.deck[choice].value != game.discard_pile[-1].value):  # Not valid
                #print("That card is not possible. Choose another. \n")
                #continue # They are prompted to choose another card

            else:   # The card is valid
                return PlaceCard(player_id, choice)

def choose_game_mode():
    try:
        game_mode = int(input("Choose a game mode by typing either '2' or '3': "))
        if game_mode < 2 or game_mode > 3:
            raise Exception
    except:
        print("That is not a valid game mode, please type it in correctly")
        return None
    else:
        return game_mode



def main():
    net = Network()   # Client connects to server

    player_id = net.receive()
    print(f"\nYou are player {player_id}")    # 0, 1 or 2

    selected_game_mode = False
    running = True

    while running:
        try:
            #n.send("get")   # To get the game
            state = net.receive()  # Receive response object containing the game

        except:
            print("\nRan into an issue when receiving the game")
            running = False

        else:
            if not selected_game_mode:
                game_mode = choose_game_mode()
                if game_mode == 3:
                   selected_game_mode = True
                   net.send(game_mode)

            elif state.game.started:   # If they chose a game mode already
                if player_id == state.game.turn:   # If it's your turn

                    state.game.display_info()
                    action = choose_card(player_id, state.game)   # Player chooses a card or draws a card

                    net.send(action)    # Send action object to server where it is executed and the game is updated
                else:   # If it's not your turn
                    #print("\nWaiting for the other player to finish their turn.\n")
                    net.send("None")    # If it's not their turn they don't send any action back
            else:
                print("\nWaiting for the game to start. \n")
                net.send("None")    # If it's not their turn they don't send any action back

main()

