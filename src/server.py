"""
    server.py

    Server for the project
"""

import time
from select import select
from threading import Thread
from multiprocessing import Process
from sys import exit
from classes import (Network,
                     Player,
                     Game)


class Server(Network):

    def __init__(self):
        super().__init__(server=True)
        self._games = []
        self._server.bind(self._ADDR)
        # self._server.setblocking(False)
        print("[STATUS] Server Started!")

        # Create a new process to listen
        listener = Process(target=self._listen,
                           daemon=True,
                           name="Listener")
        listener.start()
        self._get_cmd()

    def _get_cmd(self):
        """Get commands from the user"""

        commands = {"!exit": self._exit,
                    "!active": self._show_active}

        while True:
            cmd = input("")

            if cmd in commands:
                commands[cmd]()

    def _show_active(self):
        """Print all active games and clients"""
        print(f"[INFO] Active Games: {len(self._games)}")

    def _exit(self):
        """Exit server"""
        print("[SERVER] Exiting server!")
        exit(time.sleep(1))

    def _listen(self):
        print("[SERVER] Waiting for Clients...")
        self._server.listen(10)

        new_game = False
        while True:
            conn, addr = self._server.accept()
            # conn.setblocking(False)
            print(f"[NEW CONNECTION] Connected to Client {addr}")

            # Iterate through self._games and find
            # the game with a single player
            for game in self._games:
                if len(game.players) % 2 == 0:
                    continue
                else:
                    # Append player to the game's list
                    game.players.append(Player(""))
                    game.clients.append(conn)
                    break
            else:
                # Add client to a new game

                # Create a Game obj
                game_id = len(self._games) + 1
                game = Game(game_id)

                # Create a Player obj and add it to 'game.players' list
                game.players.append(Player(""))
                game.clients.append(conn)

                # Update the game_dict and add it to self._games
                self._games.append(game)
                new_game = True

            # Create a new thread for new games
            if new_game:
                thread = Thread(target=self._handle_game,
                                args=(game,),
                                daemon=True,
                                name=f"Thread (GameID: {game_id})")
                thread.start()
                new_game = False

    def _handle_game(self, game):
        """Handle one game"""
        pos = [0, 0]
        while True:
            # clients, _, _ = select(game.clients, [], [], 0.5)
            clients = game.clients

            for client in clients:
                data = client.recv(1024)
                if not data:
                    game.players.pop(clients.index(client))
                    game.clients.remove(client)
                    client.close()
                else:
                    data = int(data.decode("utf-8"))
                    pos[clients.index(client)] = data
                    r = client.send(
                        f"{pos[int(not (clients.index(client)))]}".encode
                        ("utf-8"))
                    if r == 0:
                        game.players.pop(clients.index(client))
                        game.clients.remove(client)
                        client.close()


def main():
    """Create Server Obj"""
    Server()


if __name__ == "__main__":
    main()
