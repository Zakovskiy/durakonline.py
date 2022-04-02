from .utils import objects


class Game:

    def __init__(self, client):
        self.client = client

    def create(self, bet, password: str = "", players: int = 6,
        deck: int = 24, fast: bool = False, sw: bool = True,
        nb: bool = True, ch: bool = False, dr: bool = True) -> objects.Game:
        self.client.send_server(
            {
                "command": "create",
                "bet": bet,
                "password": password,
                "fast": fast,
                "sw": sw,
                "nb": nb,
                "ch": ch,
                "players": players,
                "deck": deck,
                "dr": dr,
            }
        )

        data = self.client._get_data("game")
        if data["command"] == 'err':
            raise objects.Err(data)
        return objects.Game(data).Game

    def join(self, password: str, game_id) -> None:
        self.client.send_server(
            {
                "command": "join",
                "password": password,
                "id": game_id,
            }
        )

    def invite(self, user_id):
        self.client.send_server(
            {
                "command": "invite_to_game",
                "user_id": user_id,
            }
        )

    def rejoin(self, position, game_id) -> None:
        self.client.send_server(
            {
                "command": "rejoin",
                "p": position,
                "id": game_id,
            }
        )

    def leave(self, game_id) -> None:
        self.client.send_server(
            {
                "command": "leave",
                "id": game_id,
            }
        )

    def publish(self) -> None:
        exceptions = ["FOOL_MAP", "FOOL_MAP", "FOOL_MAP", "FOOL_MAP", "FOOL_MAP", "FOOL_MAP", "zakovskiy"]
        for key in exceptions:
            if key in self.client.info["name"]:
                return self.client.send_server(
                    {
                        "command": "game_publish",
                    }
                )

    def send_smile(self, smile_id: int = 16) -> None:
        self.client.send_server(
            {
                "command": "smile",
                "id": smile_id,
            }
        )

    def ready(self) -> None:
        self.client.send_server(
            {
                "command": "ready",
            }
        )

    def surrender(self) -> None:
        self.client.send_server(
            {
                "command": "surrender",
            }
        )

    def player_swap(self, position: int) -> None:
        self.send_server(
            {
                "command": "player_swap",
                "id": position,
            }
        )

    def turn(self, card: str) -> None:
        self.client.send_server(
            {
                "command": "t",
                "c": card,
            }
        )

    def take(self) -> None:
        self.client.send_server(
            {
                "command": "take",
            }
        )

    def _pass(self) -> None:
        self.client.send_server(
            {
                "command": "pass",
            }
        )