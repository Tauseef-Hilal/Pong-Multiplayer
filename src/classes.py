"""
    Classes -> [Network, Player, Game, Ball]
"""

import socket
import pickle
from constants import WIDTH, HEIGHT
from pygame import Rect, K_w, K_s


class Network:
    """Handle sockets"""

    def __init__(self, server=False) -> None:
        self._is_server = server
        self._ADDR = ("", 5050)

        if self._is_server:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self._ADDR)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                self.socket.connect(("192.168.162.31", 5050))
            except ConnectionRefusedError:
                print("[ERROR] Server down.")

    def send(self, obj, conn=None) -> int:
        if not self._is_server:
            ret = self.socket.send(pickle.dumps(obj))
        else:
            ret = conn.send(pickle.dumps(obj))

        return ret

    def receive(self, conn=None) -> object:
        if not self._is_server:
            return pickle.loads(self.socket.recv(1024))
        return pickle.loads(conn.recv(1024))

    def __repr__(self) -> str:
        if self._is_server:
            return f"<Network => Server>"
        return f"<Network => Client>"


class Player:
    """Handle a player"""

    __slots__ = ["id",
                 "name",
                 "paddle",
                 "score"]

    def __init__(self, name, player_id) -> None:
        self.id = player_id
        self.name = name
        self.paddle = None
        self.score = 0

    def move_paddle(self, keys: dict):
        """Control the paddle"""

        if keys[K_w] and self.paddle.top > 0:
            self.paddle.y -= 6
        elif keys[K_s] and self.paddle.bottom < HEIGHT:
            self.paddle.y += 6

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Player):
            return self.id == __o.id
        return False

    def __repr__(self) -> str:
        return f"<Player => ID: {self.id}, SCORE: {self.score}>"


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
        return f"<Game => ID: {self.id}, PLAYERS: {self.players}>"


class Ball(Rect):
    "Ball class"

    x_velocity = 6
    y_velocity = 6

    def animate(self):
        "Animate the ball"

        if self.left <= 0 or self.right >= WIDTH:
            self.x_velocity, self.y_velocity = 0, 0
        self.x += self.x_velocity

        if self.top <= 0 or self.bottom >= HEIGHT:
            self.y_velocity *= -1
        self.y += self.y_velocity

    def __repr__(self) -> str:
        return f"<Ball => COORDS: ({self.x}, {self.y})>"
