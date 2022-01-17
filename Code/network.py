import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 5555

        self.addr = (self.ip, self.port)
        self.client.connect(self.addr)

    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))  # send a string data to server

            # pickle.loads to de-serialize the bytes representation and return the reconstructed object

        except socket.error as e:
            print(e)

    def receive(self):
        return pickle.loads(self.client.recv(2048*3))
