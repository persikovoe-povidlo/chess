import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 25565


class Server:
    def __init__(self, host, port):
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        self.player_w = None
        self.player_b = None
        self.active_player = self.player_w
        self.socket = socket.socket()
        self.socket.bind(('127.0.0.1', 25565))
        self.socket.listen(2)

    def send_to_players(self, command):
        self.player_w.send(command.encode())
        self.player_b.send(command.encode())

    def get_connections(self):
        while self.running:
            connection, addr = self.socket.accept()
            if self.player_w is None:
                self.player_w = connection
            else:
                self.player_b = connection
            Thread(target=self.listen, args=(connection,)).start()

    def listen(self, connection):
        try:
            while self.running:
                data = connection.recv(1024).decode()
                if data == 'disconnect':
                    if connection == self.player_w:
                        self.player_w = None
                        if self.player_b:
                            self.player_b.send('disconnect'.encode())
                        self.player_b = None
                    elif connection == self.player_b:
                        if self.player_w:
                            self.player_w.send('disconnect'.encode())
                        self.player_w = None
                        self.player_b = None
                    connection.close()

                elif data == 'start_game':
                    if self.player_w and self.player_b:
                        self.send_to_players('start_game')

                elif data[0] == 'm':
                    self.send_to_players(data)
        except:
            print('connection to client lost')

    def stop(self):
        self.running = False
        self.socket.close()


if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.get_connections()
