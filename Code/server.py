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


"""def client_thread(conn, player_num, game_id):
    global connected_players
    #global games

    conn.sendall(pickle.dumps(player_num))  # To let the player know which player they are
    response = Response(games[game_id], None)
    conn.sendall(pickle.dumps(response))    # So the first loop of the while loop in client works

    while True:
        try:
            data = pickle.loads(conn.recv(2048*3))  # Receive game mode initially
            #if not data:    # If the client disconnects they don't send anything
                #break

            game = games[game_id]   # Just to make writing easier
            if game_id in games:     # If game still exists. Game deleted if client disconnects
                if data == "None":   # Client didn't do anything
                    pass    # Doesn't update game

                elif data == 3:
                    game.connected += 1     # If a player has chosen a game mode
                    response = Response(game, None)
                    games[game_id] = game

                else:   # They sent an action
                    print("Performing action")      # Just for testing
                    response = data.execute(game)     # Perform the action sent by client
                    games[game_id] = response.game    # Update game
                    print("Action Executed")

                    if response.payload == "Executed":
                        response.game.compare_card()
                        print("Compared")
                        games[game_id] = response.game  # Update response

                    #elif response.payload == "drawn" or response.payload == None:
                        #pass    # The turn isn't incremented, so they have to choose a card again

                if game.connected == 3 and not game.started:     # If 3 players have connected
                    game.start_game(3)       # This code will only happen once
                    game.started = True     # So it doesn't start multiple games
                    games[game_id] = game   # Update game for all players
                    response = Response(game, None)

                elif game.finished == True:
                    break

                conn.sendall(pickle.dumps(response))    # Send game to client

            else:   # Game doesn't exist
                raise Exception

        except socket.error as e:
            print(e)
            break

        except: # If they disconnect or the game no longer exists
            print("The game no longer exists.")     # All players in that game will disconnect
            break

    try:    # When a client exits the game
        del games[game_id]
        print(f"Closing Game: {game_id}\n")
    except:
        pass    # Game might have been deleted already

    print("Lost Connection\n")
    connected_players -= 1

    conn.close() """


"""while True:
    connection, addr = server.accept()
    print(f"Connected to {addr}")

    connected_players += 1

    game_id = (connected_players - 1 ) // 3  # For every 3 players connected it's incremented by 1 (3//2 = 1, 1//2=0)
    # 4 players : (4 - 1 ) // 3 = 1,    5 players : (5 - 1) // 3 = 1
    print(f"Current Game Id : {game_id}")

    if temp != game_id:  # When the game_id is incremented they are not equal which means a new game is needed
        player_number = 0
        games[game_id] = Uno()   # Create new game and add to the dictionary

    elif connected_players % 3 == 0:   # 3 players have joined
        player_number = 2   # Third player = Player 2

    elif connected_players == game_id + n:       # Makes the second player = player 1.  (n = 2 then 4 then 6 etc)
        player_number = 1       # If game_id = 0, P2 is when connected_players = 2. If game_Id = 1, P2 is when CP = 5,
                                # game ID = 2, P2-> CP = 8
        n += 2

    temp = game_id  # Used to find when a new game is needed

    thread = threading.Thread(target=client_thread, args=(connection, player_number, game_id))
    # When new connection occurs its given to client_thread
    thread.start()

    active_connections = threading.active_count()
    print(f"Active connections : {active_connections - 1}\n")
    # # The number of threads (clients connected) -1 since the start thread is always running. """

def close_connection(conn_list):
    for conn in conn_list:
        conn.close()     # Closes connection for all players

def play_game(game, conn_list):
    for conn in conn_list:
        conn.send(pickle.dumps("Started"))  # To let all players know that the game has begun

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
            game_id += 1    # So each game created has their own game_id
            games[game_id] = Uno()    # Create a new game for the next players











