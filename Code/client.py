from network import Network
from interface import Interface

def main():
    interface = Interface()

    sent = False
    while interface.running:
        interface.current_screen.display()  # Prompts client to login and allows them to navigate through the menus

        if not sent and interface.game_mode_choice != 0:  # If they chose a game mode & they haven't sent it to server
            net = Network()     # Connects the client to the server after they select a game mode
            net.send(interface.game_mode_choice)
            sent = True     # So the client only sends it once

            while True:
                interface.game_mode.waiting_screen()    # Displays the waiting screen

                if net.receive():   # Receives "Started" when the game has begun
                    interface.running = False
                    player_number = net.receive()   # Receive your player number from the server
                    break

    running = True

    while running:
        try:
            state = net.receive()

        except:
            print("\nRan into an issue when receiving the data.")
            running = False

        else:
            if state.game.turn == player_number:    # If it's your turn you perform an action
                interface.game_screen.action = None     # Reset the action

                if state.payload == "choose":
                    while not interface.card_chosen:   # Client hasn't chosen card yet
                        print(player_number)
                        interface.game_screen.display(player_number, state.game) # To display the game screen

                    interface.card_chosen = False   # Reset it so they can choose another card next turn

                elif state.payload == "Confirm":
                    interface.game_screen.confirm = True

                    while interface.game_screen.confirm:
                        interface.game_screen.ask()     # Asks the user if they want to place the drawn card down

                #elif state.payload == "Executed" or state.payload == None:
                    # None when they don't place down the card they picked up. "Executed" if the card was placed down.

                action = interface.game_screen.action
                net.send(action)
                alert = net.receive()   # Tells the client that the action was executed

            else:   # If it's not your turn
                while True:
                    print(player_number)    # Received "Executed" here for p3
                    interface.game_screen.display(player_number, state.game)

                    if net.receive():   # When a player has made a move you receive data
                        break   # To return to the main loop



if __name__ == "__main__":
    main()

