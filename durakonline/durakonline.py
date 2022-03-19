import sys
import socket
import json
import threading
from .utils import objects
from datetime import datetime
from loguru import logger
from .socket_listener import SocketListener

from .authorization import Authorization
from .game import Game
from .friend import Friend


class Client(SocketListener):

    def __init__(self, token: str = None, server_id: str = None, pl: str = "ios",
        debug: bool = False, tag: str = "", ip: str = None,
        port: int = None) -> None:
        super().__init__(self)
        self.api_url = "http://static.rstgames.com/durak/"
        self.pl = pl
        self.tag = tag
        self.uid = None
        self.receive = []
        self.logger = logger
        self.logger.remove()
        self.logger.add(sys.stderr, format="{time:HH:mm:ss.SSS}: {message}", level="DEBUG" if debug else "INFO")
        self.create_connection(server_id, ip, port)
        self.load_classes()
        self.authorization.sign(self.authorization.get_session_key().key)

        if token:
            self.authorization.signin_by_access_token(token)

    def load_classes(self) -> None:
        self.authorization: Authorization = Authorization(self)
        self.game: Game = Game(self)
        self.friend: Friend = Friend(self)

    def get_user_info(self, user_id: int) -> objects.UserInfo:
        self.send_server(
            {
                "command": "get_user_info",
                "id": user_id
            }
        )
        data = self._get_data("user_info")
        if data["command"] != "user_info":
            raise objects.Err(data)
        return objects.UserInfo(data).UserInfo

    def verify_purchase(self, signature, purchase_data) -> None:
        self.send_server(
            {
                "command": "verify_purchase",
                "signature": signature,
                "purchase_data": purchase_data
            }
        )

    def get_purchase_ids(self) -> None:
        self.send_server(
            {
                "command": "get_android_purchase_ids"
            }
        )
        return objects.PurchaseIds(self._get_data("android_purchase_ids")).PurchaseIds

    def get_prem_price(self) -> objects.ItemsPrice:
        self.send_server(
            {
                "command": "get_prem_price"
            }
        )
        return objects.ItemsPrice(self._get_data("prem_price")).ItemsPrice

    def get_points_price(self) -> objects.ItemsPrice:
        self.send_server(
            {
                "command": "get_points_price"
            }
        )
        return objects.ItemsPrice(self._get_data("points_price")).ItemsPrice

    def buy_prem(self, id: int = 0) -> None:
        self.send_server(
            {
                "command": "buy_prem",
                "id": f"com.rstgames.durak.prem.{id}"
            }
        )

    def buy_points(self, id: int = 0) -> dict:
        self.send_server(
            {
                "command": "buy_points",
                "id": f"com.rstgames.durak.points.{id}"
            }
        )

        return self.listen()

    def buy_asset(self, asset_id) -> None:
        self.send_server(
            {
                "command": "buy_asset",
                "id": asset_id
            }
        )

    def get_assets(self) -> objects.Assets:
        self.send_server(
            {
                "command": "get_assets"
            }
        )
        return objects.Assets(self._get_data("assets")).Assets

    def asset_select(self, asset_id) -> None:
        self.send_server(
            {
                "command": "asset_select",
                "id": asset_id
            }
        )

    def achieve_select(self, achieve_id) -> None:
        self.send_server(
            {
                "command": "achieve_select",
                "id": achieve_id
            }
        )

    def complaint(self, to_id) -> None:
        self.send_server(
            {
                "command": "complaint",
                "id": to_id,
            }
        )

    def send_user_message_code(self, code, content) -> None:
        self.send_server(
            {
                "command": "send_user_msg_code",
                "code": code,
                "msg": content
            }
        )

    def delete_message(self, message_id) -> None:
        self.send_server(
            {
                "command": "delete_msg",
                "msg_id": message_id
            }
        )

    def gift_coll_item(self, item_id: id, coll_id: str, to: int) -> dict:
        self.send_server(
            {
                "command": "gift_coll_item",
                "item_id": item_id,
                "coll_id": coll_id,
                "to_id": to
            }
        )
        return self.listen()

    def get_bets(self) -> objects.Bets:
        self.send_server(
            {
                "command": "gb"
            }
        )
        return objects.Bets(self._get_data("bets")).Bets

    def lookup_start(self, betMin: int = 100, pr: bool = False, betMax: int = 2500,
        fast: bool = True, sw: bool = True, nb: list = [False, True], ch: bool = False,
        players: list = [2, 3, 4, 5, 6], deck: list = [24, 36, 52], dr: bool = True) -> None:
        self.send_server(
            {
                "command": "lookup_start",
                "betMin": betMin,
                "pr": [pr, False],
                "betMax": betMax,
                "fast": [fast],
                "sw": [sw],
                "nb": nb,
                "ch": [ch],
                "players": players,
                "deck": deck,
                "dr": [dr],
                "status": "open"
            }
        )

    def lookup_stop(self) -> None:
        self.send_server(
            {
                "command": "lookup_stop"
            }
        )

    def get_server(self) -> None:
        self.send_server(
            {
                "command": "get_server"
            }
        )

    def update_name(self, nickname: str = None) -> None:
        self.send_server(
            {
                "command": "update_name",
                "value": nickname
            }
        )

    def save_note(self, note: str, user_id: int, color: int = 0) -> None:
        self.send_server(
            {
                "command": "save_note",
                "note": note,
                "color": color,
                "id": user_id
            }
        )

    def leaderboard_get_by_user(self, user_id, type: str = "score", season: bool = False) -> dict:
        s = "" if not season else "s_"
        self.send_server(
            {
                "command": s+"lb_get_by_user",
                "user_id": user_id,
                "type": type
            }
        )
        return self._get_data("lb")

    def leaderboard_get_top(self, type: str = "score") -> dict:
        self.send_server(
            {
                "command": "lb_get_top",
                "type": type
            }
        )
        return self._get_data("lb")

    def leaderboard_get_by_place_down(self, place: int = 20, type: str = "score") -> dict:
        self.send_server(
            {
                "command": "lb_get_by_place_down",
                "place": place,
                "type": type
            }
        )
        return self._get_data("lb")