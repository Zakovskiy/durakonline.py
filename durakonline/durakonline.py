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

class Client(SocketListener):

    def __init__(self, token: str = None, server_id: str = None, pl: str = "ios",
        debug: bool = False, language: str = "ru", tag: str = ""):
        super().__init__(self)
        self.api_url = "http://static.rstgames.com/durak/"
        self.pl = pl
        self.tag = tag
        self.language = language
        self.uid = None
        self.receive = []
        self.logger = logger
        self.logger.remove()
        self.logger.add(sys.stderr, format="{time:HH:mm:ss.SSS}: {message}", level="DEBUG" if debug else "INFO")
        self.create_connection(server_id)
        self.load_classes()
        self.authorization.sign(self.authorization.get_session_key().key)
        if token:
            self.authorization.signin_by_access_token(token)

    def load_classes(self):
        self.authorization: Authorization = Authorization(self)
        self.game: Game = Game(self)

    def get_user_info(self, user_id: int):
        self.send_server(
            {
                "command": "get_user_info",
                "id": user_id
            }
        )
        data = self._get_data("user_info")
        if data["command"] == "err":
            raise objects.Err(data)
        else:
            return objects.UserInfo(data).UserInfo

    def friend_accept(self, friend_id: int):
        self.send_server(
            {
                "command": "friend_accept",
                "id": friend_id
            }
        )

    def friend_delete(self, friend_id: int):
        self.send_server(
            {
                "command": "friend_delete",
                "id": friend_id
            }
        )
        return self._get_data("fl_delete")

    def send_friend_request(self, user_id: int):
        self.send_server(
            {
                "command": "friend_request",
                "id": user_id
            }
        )
        return self.listen()

    def verify_purchase(self, signature, purchase_data):
        self.send_server(
            {
                "command": "verify_purchase",
                "signature": signature,
                "purchase_data": purchase_data
            }
        )

    def get_purchase_ids(self):
        self.send_server(
            {
                "command": "get_android_purchase_ids"
            }
        )
        return objects.PurchaseIds(self._get_data("android_purchase_ids")).PurchaseIds

    def get_prem_price(self):
        self.send_server(
            {
                "command": "get_prem_price"
            }
        )
        return objects.ItemsPrice(self._get_data("prem_price")).ItemsPrice

    def get_points_price(self):
        self.send_server(
            {
                "command": "get_points_price"
            }
        )
        return objects.ItemsPrice(self._get_data("points_price")).ItemsPrice

    def buy_prem(self, id: int = 0):
        self.send_server(
            {
                "command": "buy_prem",
                "id": f"com.rstgames.durak.prem.{id}"
            }
        )

    def buy_points(self, id: int = 0):
        self.send_server(
            {
                "command": "buy_points",
                "id": f"com.rstgames.durak.points.{id}"
            }
        )

        return self.listen()

    def buy_asset(self, asset_id):
        self.send_server(
            {
                "command": "buy_asset",
                "id": asset_id
            }
        )

    def get_friend_list(self) -> [objects.FriendInfo]:
        self.send_server(
            {
                "command": "friend_list"
            }
        )
        friends: [objects.FriendInfo] = []
        data = self.listen()
        while data["command"] != "img_msg_price":
            if data["command"] == "fl_update":
                friends.append(objects.FriendInfo(data).FriendInfo)
            data = self.listen()

        return friends

    def get_assets(self):
        self.send_server(
            {
                "command": "get_assets"
            }
        )
        return objects.Assets(self._get_data("assets")).Assets

    def asset_select(self, asset_id):
        self.send_server(
            {
                "command": "asset_select",
                "id": asset_id
            }
        )

    def achieve_select(self, achieve_id):
        self.send_server(
            {
                "command": "achieve_select",
                "id": achieve_id
            }
        )

    def send_message_friend(self, content, to):
        self.send_server(
            {
                "command": "send_user_msg",
                "msg": content,
                "to": to
            }
        )

    def complaint(self, to_id):
        self.send_server(
            {
                "command": "complaint",
                "id": to_id,
            }
        )

    def send_user_message_code(self, code, content):
        self.send_server(
            {
                "command": "send_user_msg_code",
                "code": code,
                "msg": content
            }
        )

    def delete_messege(self, messege_id):
        self.send_server(
            {
                "command": "delete_msg",
                "msg_id": messege_id
            }
        )

    def gift_coll_item(self, item_id: id, coll_id: str, to: int):
        self.send_server(
            {
                "command": "gift_coll_item",
                "item_id": item_id,
                "coll_id": coll_id,
                "to_id": to
            }
        )
        return self.listen()

    def get_bets(self):
        self.send_server(
            {
                "command": "gb"
            }
        )
        return objects.Bets(self._get_data("bets")).Bets

    def lookup_start(self, betMin: int = 100, pr: bool = False, betMax: int = 2500, fast: bool = True, sw: bool = True, nb: list = [False, True], ch: bool = False, players: list = [2, 3, 4, 5, 6], deck: list = [24, 36, 52], dr: bool = True):
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

    def lookup_stop(self):
        self.send_server(
            {
                "command": "lookup_stop"
            }
        )

    def get_server(self):
        self.send_server(
            {
                "command": "get_server"
            }
        )

    def update_name(self, nickname: str = None):
        self.send_server(
            {
                "command": "update_name",
                "value": nickname
            }
        )

    def save_note(self, note: str, user_id: int, color: int = 0):
        self.send_server(
            {
                "command": "save_note",
                "note": note,
                "color": color,
                "id": user_id
            }
        )

    def leaderboard_get_by_user(self, user_id, type: str = "score", season: bool = False):
        s = "" if not season else "s_"
        self.send_server(
            {
                "command": s+"lb_get_by_user",
                "user_id": user_id,
                "type": type
            }
        )

    def leaderboard_get_top(self, type: str = "score"):
        self.send_server(
            {
                "command": "lb_get_top",
                "type": type
            }
        )

    def leaderboard_get_by_place_down(self, place: int = 20, type: str = "score"):
        self.send_server(
            {
                "command": "lb_get_by_place_down",
                "place": place,
                "type": type
            }
        )