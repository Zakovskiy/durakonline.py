import sys
import socket
import json

from loguru import logger
from msgspec.json import decode

from .socket_listener import SocketListener
from .utils import objects, Server
from .authorization import Authorization
from .game import Game
from .friend import Friend


class Client(SocketListener):
    def __init__(self, server_id: Server = None, debug: bool = False, tag: str = "",
                 ip: str = None, port: int = None, proxy: str = "") -> None:
        """

        :param proxy:
            proxy by format "login@password:ip:port"
        """
        super().__init__(self, proxy)
        self.tag: str = tag
        self.uid: int = None
        self.info: dict = {}
        self.logger = logger
        self.logger.remove()
        self.logger.add(sys.stderr, format="{time:HH:mm:ss.SSS}: {message}", level="DEBUG" if debug else "INFO")
        self.create_connection(server_id, ip, port)

        self.authorization: Authorization = Authorization(self)
        self.game: Game = Game(self)
        self.friend: Friend = Friend(self)

        self.authorization.sign(self.authorization.get_session_key().key)

    def update_avatar(self, file: str) -> None:
        self.send_server(
            {
                "command": "update_avatar",
                "base64": file
            }
        )

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
        return decode(json.dumps(data), type=objects.UserInfo)

    def verify_purchase(self, signature, purchase_data) -> None:
        self.send_server(
            {
                "command": "verify_purchase",
                "signature": signature,
                "purchase_data": purchase_data
            }
        )

    def get_purchase_ids(self) -> objects.PurchaseIds:
        self.send_server(
            {
                "command": "get_android_purchase_ids"
            }
        )
        response = self._get_data("android_purchase_ids")
        return decode(json.dumps(response), type=objects.PurchaseIds)

    def get_prem_price(self) -> objects.ItemsPrice:
        self.send_server(
            {
                "command": "get_prem_price"
            }
        )
        response = self._get_data("prem_price")
        return decode(json.dumps(response), type=objects.ItemsPrice)

    def get_points_price(self) -> objects.ItemsPrice:
        self.send_server(
            {
                "command": "get_points_price"
            }
        )
        response = self._get_data("points_price")
        return decode(json.dumps(response), type=objects.ItemsPrice)

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

    def buy_asset(self, asset_id: str) -> None:
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
        response = self._get_data("assets")
        return decode(json.dumps(response), type=objects.Assets)

    def asset_select(self, asset_id: str) -> None:
        self.send_server(
            {
                "command": "asset_select",
                "id": asset_id
            }
        )
        return self._get_data("uu")

    def achieve_select(self, achieve_id: str) -> None:
        self.send_server(
            {
                "command": "achieve_select",
                "id": achieve_id
            }
        )

    def get_achieves(self) -> list:
        self.send_server(
            {
                "command": "get_achieves"
            }
        )
        response = self._get_data("achieves")
        return decode(json.dumps(response), type=objects.Achieves)

    def complaint(self, user_id: int) -> None:
        self.send_server(
            {
                "command": "complaint",
                "id": user_id
            }
        )

    def send_user_message_code(self, code: str, content: str) -> None:
        self.send_server(
            {
                "command": "send_user_msg_code",
                "code": code,
                "msg": content
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
        response = self._get_data("bets")
        return decode(json.dumps(response), type=objects.Bets)

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

    def leaderboard_get_by_user(self, user_id: int, type: str = "score", season: bool = False) -> objects.Leaderboard:
        s = "" if not season else "s_"
        self.send_server(
            {
                "command": s+"lb_get_by_user",
                "user_id": user_id,
                "type": type
            }
        )
        response = self._get_data("lb")
        return decode(json.dumps(response), type=objects.Leaderboard)

    def leaderboard_get_top(self, type: str = "score", season: bool = False) -> objects.Leaderboard:
        s = "" if not season else "s_"
        self.send_server(
            {
                "command": f"{s}lb_get_top",
                "type": type
            }
        )
        response = self._get_data("lb")
        return decode(json.dumps(response), type=objects.Leaderboard)

    def leaderboard_get_by_place_down(self, place: int = 20, type: str = "score", season: bool = False) -> objects.Leaderboard:
        s = "" if not season else "s_"
        self.send_server(
            {
                "command": f"{s}lb_get_by_place_down",
                "place": place,
                "type": type
            }
        )
        response = self._get_data("lb")
        return decode(json.dumps(response), type=objects.Leaderboard)

    def shutdown(self):
        super().shutdown()

    def __del__(self):
        self.shutdown()
