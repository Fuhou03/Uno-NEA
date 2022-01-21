from network import Network
from actions import *

def choose_card(game):
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
            return DrawCard()

        except IndexError:
            print("That card is not possible. Please enter the number correctly.")
            continue    # They will have to enter again

        else:
            if (current_player.deck[choice].colour == game.discard_pile[-1].colour) or \
                    (current_player.deck[choice].value == game.discard_pile[-1].value):  # Not valid

                return CheckCard(choice)

            elif current_player.deck[choice].colour == "None":   # wildcard
                new_colour = input("Choose a colour for the next player: ")
                return CheckCard(choice, colour=new_colour)  # Colour an optional parameter

            else:
                print("That card is not possible. Choose another. \n")
                continue # They are prompted to choose another card



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
    net = Network() # To send and receive data from server

    running = True
    went = False

    while running:
        try:
            state = net.receive()


        except Exception as e:
            print("\n {str(e)} \nRan into an issue when receiving the data.")
            break

        else:
            if not state.game.started:
                game_mode = choose_game_mode()
                net.send(game_mode)
            else:
                if state.payload == "choose" and not went:   # It is their turn
                    print(f"Current turn: {state.game.turn}")
                    state.game.display_info()
                    action = choose_card(state.game)    # To tell the server to place the card down or draw a card
                    net.send(action)    # Send action to server
                    went = True

                elif state.payload == "confirm":
                    current_p = state.game.player_list[state.game.turn]
                    confirm = input(f"The {current_p.deck[-1].colour} - {current_p.deck[-1].value}"
                    f" card you picked up is valid, do you want to place it down? Type 'y' or 'n': ")

                    net.send(PlaceCard(confirm))

                elif state.payload == "executed":
                    went = False    # So they can choose another card when it is their turn again



main()

