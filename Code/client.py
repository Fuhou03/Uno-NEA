from network import Network
from actions import *
from interface import Interface
import pygame

def choose_card(game):
    """ To choose your own card """

    # game.player_list[game.turn] is the Current Player

    valid = False
    while not valid:
        try:
            choice = int(input("\nChoose a card by typing it's number at the front. \n"
                               "If you have no valid cards then type any string to draw a card: "))
            print("")
            if choice >= len(game.player_list[game.turn].deck) or choice < 0:  # If they enter an invalid number
                raise IndexError

        except ValueError:  # If they entered a string
            return DrawCard()

        except IndexError:
            print("That card is not possible. Please enter the number correctly.")
            continue    # They will have to enter again

        else:
            if (game.player_list[game.turn].deck[choice].colour == game.discard_pile[-1].colour) or \
                    (game.player_list[game.turn].deck[choice].value == game.discard_pile[-1].value):  # Not valid

                return PlaceCard(choice)

            elif game.player_list[game.turn].deck[choice].colour == None:   # wildcard
                new_colour = input("Choose a colour for the next player: ")
                return PlaceCard(choice, colour=new_colour)  # Colour is an optional parameter

            else:   # The card they pick does not match in colour or value
                print("That card is not possible. Choose another. \n")
                continue # They are prompted to choose another card


def main():
    net = Network() # To send and receive data from server
    interface = Interface()

    while interface.running:
        interface.current_screen.display()  # Prompts client to login and allows them to navigate through the menus

    pygame.quit()
    net.send(interface.game_mode_choice)    # Sends their selected game mode to the server


    running = True
    went = False

    while running:
        try:
            state = net.receive()

        except:
            print("\nRan into an issue when receiving the data.")
            break

        else:
            if state.game.started:
                if state.payload == "choose" and not went:   # It is their turn
                    state.game.display_info()
                    action = choose_card(state.game)    # Used to tell the server to place the card down or draw a card
                    net.send(action)    # Send action to server
                    went = True     # So they cannot place another card down

                elif state.payload == "confirm":
                    #current_p = state.game.player_list[state.game.turn]
                    confirm = input(f"The {state.game.player_list[state.game.turn].deck[-1].colour}"
                                    f" - {state.game.player_list[state.game.turn].deck[-1].value}"
                    f" card you picked up is valid, do you want to place it down? Type 'y' or 'n': ")

                    net.send(Decision(confirm))
                    went = True

                elif state.payload == "Executed" or state.payload == None:
                    # None when they don't place down the card they picked up. "Executed" if the card was placed down.
                    print(f"Current turn: {state.game.turn}")
                    went = False    # So they can choose another card when it is their turn again



main()

