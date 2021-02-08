import socket
"""connexion en multijoueur"""

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return True
        except:
            return False

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def get_player_number(self):
        try:
            self.client.send(str.encode("p"))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            return False

#n = Network()
#connection = n.get_player_number()
#print(connection)
#print(n.send("ok"))
#print(connection)