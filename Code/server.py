import socket
import threading
import pickle
from game import Uno
from actions import Response

ip = socket.gethostbyname(socket.gethostname())  # my IPv4 Address
port = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (ip, port)

print("Server is starting")
try:
    server.bind(ADDR)
except socket.error as e:
    str(e)

server.listen()  # lets multiple clients connect (2 people)
print("Waiting for a connection\n")


def close_connection(conn_list):
    for conn in conn_list:
        conn.close()     # Closes connection for all players

def play_game(game, conn_list):
    waiting = True
    while waiting:
        for conn in conn_list:
            game_mode = pickle.loads(conn.recv(2048*2))     # Receive the game mode chosen by client

            if game_mode == 3:
                game.connections += 1

                if game.connections == 3:
                    game.start_game(game_mode)   # Begin the game once 3 players chose the same game mode
                    game.started = True
                    waiting = False

    while True:
        conn = conn_list[game.turn]     # Get the connection of the player whose turn it is

        response = Response(game, "choose")
        conn.send(pickle.dumps(response))     # Sending the game to the client

        try:
            data = pickle.loads(conn.recv(2048*3))  # Receiving data from client
        except:
            print("A player has left so the game will stop.")
            close_connection(conn_list)
            break
        else:
            response = data.execute(game)
            print("\nAction Executed")    # Just for testing

            if response.payload == "Executed":
                response.game.compare_card()
                print("Compared")

            game = response.game    # Update the game so it can be sent to the next player
            if game.finished:   # Player placed down their final card
                close_connection(conn_list)
                break

            print(f"Turn: {game.turn}")
            conn.send(pickle.dumps(response))


games = {}  # Dictionary to store the game id along with the associated game object
conn_list = []
game_id = 1
player_id = 0

games[game_id] = Uno()  # Creating the first game

while True:
    connection, addr = server.accept()
    print(f"Connected to {addr}")
    print(f"Current Game Id : {game_id}\n")

    games[game_id].add_player(player_id)    # To create a new player inside the game
    conn_list.append(connection)

    if games[game_id].connected == 3:   # 3 players have joined (it's incremented when add_player is called)
        thread = threading.Thread(target=play_game, args=(games[game_id], conn_list))   # Create a new thread for every game
        thread.start()

        game_id += 1    # This is the dictionary key
        games[game_id] = Uno()    # Create a new game for the next 3 players that join
        player_id = 0   # Reset
        conn_list = []

    else:
        player_id += 1  # Increments by 1 every time a new player joins (until it becomes 3 and the game begins)








