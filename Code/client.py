import pygame
from network import Network
import pickle


def main():
    net = Network()   # Client connects to server

    player_id = net.receive()
    print(f"You are player {player_id}")    # 0, 1 or 2

    selected_game_mode = False
    running = True

    while running:
        try:
            game = net.receive()  # Receive game object

        except:
            print("\nRan into an issue when receiving the game!")
            running = False

        else:
            if not selected_game_mode:
                try:
                    game_mode = int(input("Choose a game mode by typing either '2' or '3': "))
                    if game_mode < 2 or game_mode > 3:
                        raise Exception

                except:
                    print("That is not a valid game mode, please type it in correctly")

                else:
                    if game_mode == 3:
                        game.connected += 1
                        selected_game_mode = True

            if game.started:
                player = game.player_list[player_id]    # Get your player object from the game
                game.current_player = player
#
                if player.id == game.turn:   # If it's your turn
                    game.display_info()
                    game.choose_card(player)   # Player chooses card
                    game.compare_card()

                    if game.drew_card:
                        game.choose_card(player)    # Checks if the card they picked up can be placed down
                        game.drew_card = False
                else:
                    print("\nWaiting for the other player to finish their turn.\n")



            net.send(game)    # Return game back to server so it can be sent back to the other clients






main()

