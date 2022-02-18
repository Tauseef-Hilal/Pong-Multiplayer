"""
    server.py

    Server for the project
"""

import time
from sys import exit
from threading import Thread
from classes import Network, Player, Game


class Server(Network):

    def __init__(self):
        super().__init__(server=True)
        self._games = []
        self._client_count = 0
        print("[STATUS] Server Started!")

        # Create a new thread for listening
        listener = Thread(target=self._listen,
                          daemon=True,
                          name="Listener")
        listener.start()

        # Start server terminal
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
        print(f"[INFO] Active Clients: {self._client_count}")

    def _exit(self):
        """Exit server"""
        print("[SERVER] Exiting server!")
        exit(time.sleep(1))

    def _listen(self):
        print("[SERVER] Waiting for Clients...")
        self.server.listen(10)

        new_game = False
        while True:
            conn, _ = self.server.accept()
            print(f"[INFO] Client {conn.getsockname()} connected.")

            # Iterate through self._games and find
            # the game with a single player
            for game in self._games:
                if len(game.players) % 2 == 0:
                    continue
                else:
                    # Create player obj and append it to 'game.players' list
                    player_name = "X" if game.players[-1].name == "Y" else "Y"
                    player_id = f"[{self._client_count + 1}]"

                    game.players.append(Player(player_name, player_id))
                    game.clients.append(conn)
                    break

            # If no vacancies, add player to a new game
            else:
                # Create a Game obj
                game_id = len(self._games) + 1
                game = Game(game_id)

                # Create a Player obj and add it to 'game.players' list
                game.players.append(Player("X", f"[{self._client_count + 1}]"))
                game.clients = [conn]

                # Add the game to self._games
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

            # Update client counter
            self._client_count += 1

    def _handle_game(self, game):
        """Handle one game"""

        players = [0, 0]
        temp = 1

        while True:
            clients = game.clients[:]

            for client_idx, client in enumerate(clients):
                try:
                    data = self.receive(conn=client)
                except EOFError:
                    data = None

                if data and data == "!get":
                    players[client_idx] = game.players[client_idx]
                    temp = self.send(players[client_idx], client)
                else:
                    players[client_idx if len(clients) == 2 else -1] = data
                    temp = self.send(players[int(not client_idx)], client)

                if not data or temp == 0:
                    players[client_idx] = 0

                    print("[INFO] Client",
                          f"{client.getsockname()} disconnected.")

                    game.players.pop(client_idx)
                    game.clients.remove(client)
                    client.close()

                    self._client_count -= 1
                    if not game.players:
                        self._games.remove(game)
                        break


def main():
    """Create Server Obj"""
    Server()


if __name__ == "__main__":
    main()
