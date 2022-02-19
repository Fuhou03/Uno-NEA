import socket
import threading
import pickle
from game import Uno
from actions import Response
import time

ip = socket.gethostbyname(socket.gethostname())  # my IPv4 Address
port = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (ip, port)

print("Server is starting")
try:
    server.bind(ADDR)
except socket.error as e:
    print(e)

server.listen()  # lets multiple clients connect
print("Waiting for a connection\n")


def close_connection(connections):
    """ Closes connection for all players """
    for conn in connections:
        conn.close()     # Closes connection for all players
        time.sleep(0.1)


def play_game(game, con_list):
    conn_list = con_list
    for num in range(0, len(conn_list)):  # To get the connections of each client
        conn_list[num].sendall(pickle.dumps("Started"))  # To let all players know that the game has begun
        time.sleep(0.05)
        conn_list[num].sendall(pickle.dumps(num))  # To let the player know which number they are
        time.sleep(0.1)     # Short delay stops data being sent to wrong client

    running = True
    confirming = False

    while running:
        if not confirming:  # If it's waiting for the player to confirm their choice it doesn't send anything
            for conn in conn_list:
                response = Response(game, "Choose")     # So the client selects a card if it's their turn
                conn.sendall(pickle.dumps(response))     # Sending the game and payload to the client
                print(f"Sent data to {conn_list.index(conn)}")
                time.sleep(0.1)

        try:
            data = pickle.loads(conn_list[game.turn].recv(2048*3))  # Receiving data from the current player
        except Exception as e:
            print(e)
            print("A player has left so the game will stop.")
            close_connection(conn_list)
            running = False

        confirming = False  # Reset it in case a player was asked to confirm their choice before
        response = data.execute(game)   # Calls the execute method of the action
        # E.g. Executing the PlaceCard action removes the card from the player's deck and adds it to the discard pile

        if response.payload == "Executed":  # If they placed a card down
            # Checks which card was selected and performs the action
            response.game.compare_card()    # E.g Draw 2 skips the next player and deals them 2 cards

            if game.finished:   # Player placed down their final card
                close_connection(conn_list)
                running = False

        elif response.payload == "Confirm":   # If the player drew a card they'll be asked if they want to place it down
            confirming = True   # So the server doesn't ask the client to choose another card until they've confirmed

        game = response.game    # Update the game so the updated version is sent to all players

        if not confirming:
            for conn in conn_list:
                conn.sendall(pickle.dumps(response.payload)) # So all clients receive the response below at the same time
                time.sleep(0.05)
                conn.sendall(pickle.dumps(response))   # Send the game back to all clients
                time.sleep(0.1)
        else:   # When confirming with the current player it only sends data to them so that the other players will wait
            conn_list[game.turn].sendall(pickle.dumps(response.payload))
            conn_list[game.turn].sendall(pickle.dumps(response))

        time.sleep(0.1)


games = {}  # Dictionary to store the game id along with the corresponding game object
conn_list = []

game_id = 1
player_id = 0

games[game_id] = Uno()  # Creating a game for the first group of players

game_mode_dict = {}
game_mode_dict[2] = []
game_mode_dict[3] = []
game_mode_dict[4] = []

while True:
    connection, addr = server.accept()
    print(f"\n{addr = }")
    print(f"{game_id = }")

    game_mode = pickle.loads(connection.recv(2048*2))     # Receive game mode choice

    # Adds the connection of the player into a list depending on their choice
    game_mode_dict[game_mode].append(connection)

    for game_mode in game_mode_dict:   # To begin the game when enough players have chosen that game mode
        if len(game_mode_dict[game_mode]) == game_mode:     # E.g If 3 players have chosen Three Player mode

            for i in range(0, len(game_mode_dict[game_mode])):
                games[game_id].add_player(i)    # Create the players inside the game

            games[game_id].start_game(len(game_mode_dict[game_mode]))
            # Tells the game object which game mode was selected

            thread = threading.Thread(target=play_game, args=(games[game_id], game_mode_dict[game_mode]))
            thread.start()  # Each game will play in their own thread so multiple games can play at the same time

            game_mode_dict[game_mode] = []  # Clear the list so new players can also play that game mode
            game_id += 1    # So the next game created has a different game_id
            games[game_id] = Uno()    # Create a new game for the next players











