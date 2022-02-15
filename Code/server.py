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
        time.sleep(0.2)

def play_game(game, conn_list):
    for num in range(0, len(conn_list)):  # To get the connections of each client
        conn_list[num].send(pickle.dumps("Started"))  # To let all players know that the game has begun
        conn_list[num].send(pickle.dumps(num))  # To let the player know which number they are
        time.sleep(0.2)     # Short delay stops data being sent to wrong client

    running = True
    confirming = False

    while running:
        if not confirming:  # If it's waiting for the player to confirm their choice it doesn't send anything
            for conn in conn_list:
                response = Response(game, "Choose")     # So the client selects a card if it's their turn
                conn.send(pickle.dumps(response))     # Sending the game and payload to the client
                print(f"Sent data to {conn_list.index(conn)}")
                time.sleep(0.3)

        try:
            data = pickle.loads(conn_list[game.turn].recv(2048*3))  # Receiving data from the current player
        except Exception as e:
            print(e)
            print("A player has left so the game will stop.")
            close_connection(conn_list)
            running = False

        #else:
        confirming = False
        response = data.execute(game)
        print("\nAction Executed")    # Just for testing

        if response.payload == "Executed":
            response.game.compare_card()
            print("Compared")

            if game.finished:   # Player placed down their final card
                close_connection(conn_list)
                running = False

        elif response.payload == "Confirm":
            confirming = True

        game = response.game    # Update the game so the updated version is sent to all players

        for conn in conn_list:
            conn.send(pickle.dumps("Executed"))    # So all clients receive next line at try statement
            #time.sleep(0.1)
            conn.send(pickle.dumps(response))   # Send the game back to all clients
            time.sleep(0.2)

        time.sleep(0.2)

games = {}  # Dictionary to store the game id along with the associated game object
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









