import socket
import pickle
from interface import Interface


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = socket.gethostbyname(socket.gethostname())
       
        self.port = 5555

        self.addr = (self.ip, self.port)
        self.client.connect(self.addr)

    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))  # Sends data to the server

        except socket.error as e:
            print(e)

    def receive(self):
        return pickle.loads(self.client.recv(2048*3))
        # pickle.loads to de-serialize the data which is in bytes format, and return the reconstructed object


def main():
    interface = Interface()

    sent = False
    while interface.running:
        interface.current_screen.display()  # Prompts client to login and allows them to navigate through the menus

        if not sent and interface.game_mode_choice != 0:  # If they chose a game mode & they haven't sent it to server
            net = Network()     # Connects the client to the server after they select a game mode
            net.send(interface.game_mode_choice)
            sent = True     # So the client only sends it once
            net.client.setblocking(False)   # Set socket into non-blocking mode so the loop doesn't pause

            while True:
                interface.game_mode.waiting_screen()    # Displays the waiting screen

                try:
                    # This would pause the loop until it receives data if it was in blocking-mode
                    if net.receive():   # Receives data when the game has begun so it can stop the loop
                        net.client.setblocking(True)    # Reset it so it waits to receive the player number

                except:     # An error occurs when no data is received
                    pass    # So the loop continues without pausing

                else:
                    player_number = net.receive()   # Receive your player number from the server
                    interface.running = False
                    break

    running = True

    while running:
        try:
            state = net.receive()

        except Exception as e:
            print(e)
            print("\nRan into an issue when receiving the data.")
            running = False

        if state.game.finished:
            running = False
            interface.game_screen.finished_screen(state.game)

        if state.game.turn == player_number:    # If it's your turn you perform an action
            if state.payload == "Choose":
                while not interface.card_chosen:   # Client hasn't chosen card yet
                    interface.game_screen.display(player_number, state.game) # To display the game screen

                interface.card_chosen = False   # Reset it so they can choose another card next turn

            elif state.payload == "Confirm":
                interface.game_screen.confirm = True
                while interface.game_screen.confirm:
                    interface.game_screen.ask(state.game)     # Asks the user if they want to place the drawn card down

            if state.payload == "Choose" or state.payload == "Confirm":
                # == 'None' when they don't place down the card they picked up, 'Executed"' if the card was placed down
                action = interface.game_screen.action
                net.send(action)    # Send the action to the server so it can be executed

                interface.game_screen.action = None     # Reset the action
                alert = net.receive()   # To tell the client that the action was executed
                # alert is needed so all clients can return to the try statement at the same time and receive the game

        else:   # If it's not your turn
            net.client.setblocking(False)   # Stops the client socket from breaking the loop if it receives no data
            if state.payload == "Choose":   # Displays the game screen, but they won't be able to pick a card
                while True:
                    interface.game_screen.display(player_number, state.game)

                    try:
                        msg = net.receive()
                        # When a player has made a move you receive a message which breaks the loop
                        if msg == "Executed" or "None":    # If a player is confirming their action you will wait
                            break   # To return to the main loop
                    except:
                        pass    # Stops the loop from breaking when no data is received

            else:   # If an action was just executed it moves on and waits to receive the game again
                pass

            net.client.setblocking(True)
            # Resetting it to True, so the program waits at the top try statement until the client receives the game

if __name__ == "__main__":
    main()

