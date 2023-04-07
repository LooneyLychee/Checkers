from multiprocessing.connection import Client
import socket

class Network:
    def __init__(self, data):
        self.client = None
        # self.server = "172.104.158.227"
        self.server = server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect(data)

    def get_p(self):
        return self.p

    def connect(self, data):
        try:
            self.client = Client(self.addr)
            self.client.send(data)
            return self.client.recv()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(data)
            return self.client.recv()
        except:
            print("conn failed")
