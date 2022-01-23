from network import Network
from actions import *
from interface import Interface

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


def main():
    net = Network() # To send and receive data from server
    interface = Interface()
    while interface.running:
        interface.current_screen.display()  # Prompts client to login and allows them to navigate through the menus

    running = True
    went = False

    while running:
        try:
            state = net.receive()

        except:
            print("\nRan into an issue when receiving the data.")
            break

        else:
            if not state.game.started:
                game_mode = interface.game_mode_choice     # Either 2, 3 or 4
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

