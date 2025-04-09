import socket
from threading import Thread
from random import randint

HOST = '127.0.0.1'
PORT = 25565


class Server:
    def __init__(self, host, port):
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        self.player1 = None
        self.player2 = None
        self.active_player = self.player1
        self.socket = socket.socket()
        self.socket.bind(('127.0.0.1', 25565))
        self.socket.listen()

    def send_to_players(self, command):
        self.player1.send(command.encode())
        self.player2.send(command.encode())

    def get_connections(self):
        while self.running:
            connection, addr = self.socket.accept()
            if self.player1 is None and self.player2 is None:
                if randint(0, 1):
                    self.player1 = connection
                else:
                    self.player2 = connection
            elif self.player1 is None:
                self.player1 = connection
            elif self.player2 is None:
                self.player2 = connection
            else:
                connection.send('disconnect'.encode())
                connection.close()
                return
            Thread(target=self.listen, args=(connection,)).start()

    def listen(self, connection):
        try:
            while self.running:
                data = connection.recv(10).decode()
                if data == 'disconnect':
                    if connection == self.player1:
                        self.player1 = None
                        if self.player2:
                            self.player2.send('disconnect'.encode())
                        self.player2 = None
                    elif connection == self.player2:
                        if self.player1:
                            self.player1.send('disconnect'.encode())
                        self.player1 = None
                        self.player2 = None
                    connection.close()

                elif data == 'start_game':
                    self.player1, self.player2 = self.player2, self.player1
                    if self.player1 and self.player2:
                        self.player1.send('start w'.encode())
                        self.player2.send('start b'.encode())

                elif data[0] == 'm':
                    self.send_to_players(data)

                elif data[0] == 'n':
                    self.send_to_players(data)

                elif data == 'undo':
                    self.send_to_players(data)
        except:
            connection.close()
            print('connection to client lost')

    def stop(self):
        self.running = False
        self.socket.close()


if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.get_connections()
