import socket
import threading
import pickle
from game import Uno

ip = socket.gethostbyname(socket.gethostname())  # my IPv4 Address
port = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (ip, port)

games = {}  # Dictionary to store the game id along with the associated game object
three_player_count = 0
connected_players = 0
game_id = 0
player_number = 0
temp = 1
n = 2   # Used to find the 2nd player

print("Server is starting")
try:
    server.bind(ADDR)
except socket.error as e:
    str(e)

server.listen()  # lets multiple clients connect (2 people)
print("Waiting for a connection\n")


def client_thread(conn, player_num, game_id):
    global connected_players
    conn.sendall(pickle.dumps(player_num))  # To let the player know which player they are

    #    conn.sendall(pickle.dumps(game))  # Sends the game so the client can choose a game mode
    #    game = pickle.loads(conn.recv(2048*3))      # To check if 3 players have connected

    while True:
        game = games[game_id]
        try:
            if game_id in games:     # If game still exists. Game deleted if client disconnects
                conn.sendall(pickle.dumps(game))    # Send game to client
                game = pickle.loads(conn.recv(2048*3))

            else:
                raise Exception

        except socket.error as e:
            print(e)

        except: # If they disconnect or the game no longer exists
            print("The game no longer exists.")     # All players in that game will disconnect
            break

        else:
            if game.connected != 3:
                print(f"Game connected: {game.connected}")

            if game.connected == 3 and not game.started:     # If 3 players have connected
                game.play_game(3)       # This code will only happen once
                game.started = True     # So it doesn't start multiple games

            elif game.finished == True:
                break


    try:    # Game might have been deleted already
        del games[game_id]
        print(f"Closing Game: {game_id}\n")
    except:
        pass

    print("Lost Connection\n")
    connected_players -= 1

    conn.close()


while True:
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
        player_number = 1       # If game_id = 0, P2 is when CP = 2. game_Id = 1, P2 is when CP = 5, GID = 2, P2-> CP = 8
        n += 2

    temp = game_id  # Used to find when a new game is needed

    thread = threading.Thread(target=client_thread, args=(connection, player_number, game_id))
    # When new connection occurs its given to client_thread
    thread.start()

    active_connections = threading.active_count()
    print(f"Active connections : {active_connections - 1}\n")
    # # The number of threads (clients connected) -1 since the start thread is always running.




