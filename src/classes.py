"""
    Network class
"""

import socket
import pickle


class Network:
    """Handle sockets"""

    def __init__(self, server=False) -> None:
        self.is_server = server
        self._ADDR = ("", 5050)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not self.is_server:
            self._server.connect(self._ADDR)

    def send(self, obj, conn=None) -> None:
        if not self.is_server:
            self._server.sendall(pickle.dumps(obj))
        else:
            conn.sendall(pickle.dumps(obj))

    def receive(self, conn=None) -> object:
        if not self.is_server:
            return pickle.loads(self._server.recv(4096))
        return pickle.loads(conn.recv(4096))

    def __repr__(self) -> str:
        if self.is_server:
            return f"<Network => Server>"
        return f"<Network => Client>"


class Player:
    """Handle a player"""

    __slots__ = ["name",
                 "score"]

    def __init__(self, name) -> None:
        self.name = name
        self.score = 0

    def __repr__(self) -> str:
        return f"Player({self.name}, {self.score})"


class Game:
    """Game class"""

    __slots__ = ["id",
                 "clients",
                 "players"]

    def __init__(self, id) -> None:
        self.id = id
        self.clients = []
        self.players = []

    def __repr__(self) -> str:
        return f"Game({self.id}, {self.players})"
