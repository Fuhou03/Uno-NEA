import socket
import threading
import pickle
from game import Uno
from actions import Response
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())  # my IPv4 Address

port = 5555

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
        time.sleep(0.05)    # A delay is needed as the client would not be ready to receive the data yet (error occurs)
        conn_list[num].sendall(pickle.dumps(num))  # To let the player know which number they are
        time.sleep(0.1)     # Short delay stops data being sent to wrong client

    running = True
    confirming = False
    data = None

    while running:
        if not confirming:  # If it's waiting for the player to confirm their choice it doesn't send anything
            for conn in conn_list:
                # Every player receives a request from the server but only if it's their turn, they will send data back
                response = Response(game, "Choose")
                conn.sendall(pickle.dumps(response))     # Telling the clients to select or draw a card
                # Send a response object to the client which contains the game and an additional message (payload)
                # On the client side, the player whose turn it is will send their action back to the server
                time.sleep(0.1)

        try:    # Could add a timer here
            data = pickle.loads(conn_list[game.turn].recv(2048*3))  # Receiving the action from the current player

        except Exception as e:
            print(e)
            print("A player has left so the game will stop.")
            close_connection(conn_list)
            running = False

        else:
            confirming = False  # Reset it in case a player was asked to confirm their choice before

            response = data.execute(game)   # Calls the execute method of the action and the updated game is returned
            # E.g Executing the PlaceCard action removes the card from the player's deck and adds it to the discard pile

            if response.payload == "Executed":  # If they placed a card down
                # Checks which card was selected and performs the necessary action:
                response.game.compare_card()    # e.g A Draw 2 card skips the next player and deals them 2 cards

            elif response.payload == "Confirm":
                # If the player drew a card they'll be asked if they want to place it down
                confirming = True   # So the server doesn't ask the current player to choose another card
                # until they've confirmed if they want to place the card they drew down or not

            game = response.game    # Update the game so the updated version is sent to all players

            if not confirming:
                for conn in conn_list:
                    conn.sendall(pickle.dumps(response.payload))
                    # To synchronise all clients so they receive the game below at the same time ^
                    time.sleep(0.05)    # Delays ensure the clients are ready to receive data before it is sent
                    conn.sendall(pickle.dumps(response))   # Send the game along with a message back to all clients
                    time.sleep(0.1)

            else:
                # When the current player is confirming, it only sends data to them so that the other players will wait
                conn_list[game.turn].sendall(pickle.dumps(response.payload))
                conn_list[game.turn].sendall(pickle.dumps(response))
                time.sleep(0.1)

            if game.finished:   # Player placed down their final card
                close_connection(conn_list)
                running = False


games = {}  # Dictionary to store the game id along with the corresponding game object
conn_list = []

game_id = 1
player_id = 0

games[game_id] = Uno()  # Creating a game for the first group of players

game_mode_dict = {2: [],
                  3: [],
                  4: []}    # Every game mode has their own list to store the player's connection

while True:
    connection, addr = server.accept()
    print(f"\n{addr = }")
    print(f"{game_id = }")

    game_mode = pickle.loads(connection.recv(2048*2))     # Receive every client's game mode choice
    print(f"{game_mode = }")

    # Adds the connection of the player into a list depending on their choice
    game_mode_dict[game_mode].append(connection)

    for game_mode in game_mode_dict:   # To begin the game when enough players have chosen that game mode
        if len(game_mode_dict[game_mode]) == game_mode:     # E.g If 3 players have chosen Three Player mode

            for i in range(0, len(game_mode_dict[game_mode])):
                games[game_id].add_player(i)    # Create the players inside the game

            games[game_id].start_game(len(game_mode_dict[game_mode]))
            # Tells the game object which game mode was selected and deals cards to each player

            thread = threading.Thread(target=play_game, args=(games[game_id], game_mode_dict[game_mode]))
            thread.start()  # Creates and starts a new thread
            # Each game will play in their own thread so multiple games can play at the same time

            game_mode_dict[game_mode] = []  # Clear the list so new players can also play that game mode
            game_id += 1    # So the next game created has a different game_id
            games[game_id] = Uno()    # Create a new game for the next players












