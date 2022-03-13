import base64
import hashlib
from datetime import datetime
from .utils import objects


class Authorization:

    def __init__(self, client) -> None:
        self.client = client

    def get_session_key(self) -> objects.GetSessionKey:
        data = {
            "command": "c",
            "l": self.client.language,
            "tz": "+02:00",
            "t": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z",
            "pl": self.client.pl,
            "p": 10,
        }
        if self.client.pl == "ios":
            data.update({
                "v": "1.9.1.2",
                "ios": "14.4",
                "d": "iPhone8,4",
                "n": "durak.ios",
            })
        else:
            data.update({
                "v": "1.9.2",
                "d": "xiaomi cactus",
                "and": 28,
                "n": f"durak.{self.client.pl}",
            })
        self.client.send_server(data)
        return objects.GetSessionKey(self.client.listen()).GetSessionKey

    def sign(self, key: str) -> dict:
        hash = base64.b64encode(hashlib.md5(
            (key+"oc3q7ingf978mx457fgk4587fg847").encode()).digest()).decode()
        self.client.send_server(
            {
                "command": "sign",
                "hash": hash,
            }
        )
        return self.client.listen()

    def signin_by_access_token(self, token: str) -> int:
        self.client.token = token
        self.client.send_server(
            {
                "command": "auth",
                "token": self.client.token,
            }
        )
        authorized = self.client.listen()
        if authorized["command"] == "err":
            raise objects.Err(authorized)
        self.client.uid = authorized["id"]
        return authorized["id"]

    def google_auth(self, id_token: str) -> dict:
        self.client.send_server(
            {
                "command": "durak_google_auth",
                "id_token": id_token,
            }
        )
        return self.client.listen()

    def get_captcha(self) -> dict:
        self.client.send_server(
            {
                "command": "get_captcha",
            }
        )
        return self.client._get_data("captcha")

    def register(self, name, captcha: str = '') -> objects.Register:
        self.client.send_server(
            {
                "command": "register",
                "name": name,
                "captcha": captcha,
            }
        )
        return objects.Register(self.client._get_data("set_token")).Register