"""
    server.py

    Server for the project
"""

import time
# from select import select
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
        # self.server.setblocking(False)
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
        self.server.listen(10)

        new_game = False
        while True:
            conn, addr = self.server.accept()
            # conn.setblocking(False)
            print(f"[NEW CONNECTION] Connected to Client: {addr}")

            # Iterate through self._games and find
            # the game with a single player
            for game_dict in self._games:
                if len(game_dict["game"].players) % 2 == 0:
                    continue
                else:
                    # Append player to the game's list
                    game_dict["game"].players.append(Player("R"))
                    game_dict["clients"].append(conn)
                    break
            else:
                # Add client to a new game
                game_dict = {}

                # Create a Game obj
                game_id = len(self._games) + 1
                game = Game(game_id)

                # Create a Player obj and add it to 'game.players' list
                game.players.append(Player("L"))

                game_dict["game"] = game
                game_dict["clients"] = [conn]

                # Update the game_dict and add it to self._games
                self._games.append(game_dict)
                new_game = True

            # Create a new thread for new games
            if new_game:
                thread = Thread(target=self._handle_game,
                                args=(game_dict,),
                                daemon=True,
                                name=f"Thread (GameID: {game_id})")
                thread.start()
                new_game = False

    def _handle_game(self, game_dict):
        """Handle one game"""
        game = game_dict["game"]
        players = [0, 0]
        temp = 1
        while True:
            # clients, _, _ = select(game.clients, [], [], 0.5)
            clients = game_dict["clients"]

            for client_idx, client in enumerate(clients):
                try:
                    data = self.receive(conn=client)
                except EOFError:
                    data = None

                if data:
                    # print(type(data), data)

                    if data == "!get":
                        # print("sent player")
                        players[client_idx] = game.players[client_idx]
                        temp = self.send(players[client_idx], client)
                    else:
                        # print(players)
                        players[client_idx] = data
                        # print(players[int(not client_idx)])
                        temp = self.send(players[int(not client_idx)], client)

                if not data or temp == 0:
                    game.players.pop(client_idx)
                    players[client_idx] = 0
                    game_dict["clients"].remove(client)
                    print(f"[DISCONNECTED] {client.getpeername()}")
                    client.close()


def main():
    """Create Server Obj"""
    Server()


if __name__ == "__main__":
    main()
