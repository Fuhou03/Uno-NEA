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


def play_game(game, conn_list):
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

games[game_id] = Uno()  # Creating the first game

two_player = []
three_player = []
four_player = []
game_modes = [two_player, three_player, four_player]

while True:
    connection, addr = server.accept()
    print(f"Connected to {addr}")
    print(f"Current Game Id : {game_id}\n")

    game_mode = pickle.loads(connection.recv(2048*2))     # Receive game mode choice

    if game_mode == 2:      # Adds the connection of the player into a list depending on their choice
        two_player.append(connection)
    elif game_mode == 3:
        three_player.append(connection)
    else:
        four_player.append(connection)

    for game_mode_list in game_modes:   # Create a new thread for every new game
        if game_mode_list == two_player and len(game_mode_list) == 2 or \
                game_mode_list == three_player and len(game_mode_list) == 3 or \
                game_mode_list == four_player and len(game_mode_list) == 4:   # If all players have connected

            for i in range(0, len(game_mode_list)):
                games[game_id].add_player(i)    # Create the required no. of players inside the game

            games[game_id].start_game(len(game_mode_list))  # Choose the correct game mode (takes an int as a parameter)
            games[game_id].started = True       # Begin the game

            thread = threading.Thread(target=play_game, args=(games[game_id], game_mode_list))
            thread.start()  # Each game will play in their own thread so multiple games can play at the same time

            game_mode_list = []     # Empty the list for new players can join
            game_id += 1    # So the next game created has a different game_id
            games[game_id] = Uno()    # Create a new game for the next players











