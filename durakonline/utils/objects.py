from msgspec import Struct
from typing import List, Optional
from .enums import Kind, Group


class Err(Exception):
    def __init__ (self, data:dir):
        self.json = data
        self.code = data.get("code", None)


class FormatLanguage(Struct):
    ru: str
    en: str


class GetSessionKey(Struct):
    key: str


class Server(Struct):
    time: str
    id: int


class SigninByAccessToken(Struct):
    id: int


class Register(Struct):
    token: str


class User(Struct):
    id: int
    name: str
    avatar: Optional[str]
    dtp: str
    frame: str
    achieve: str
    pw: int


class FriendInfo(Struct):
    user: User
    kind: Kind
    new: bool


class UserInfo(Struct):
    id: int
    name: str
    avatar: Optional[str]
    pw: int
    wins: int
    points_win: int
    score: int
    dtp: str
    frame: str
    achieve: str
    t_bronze: int = 0
    t_silver: int = 0
    t_gold: int = 0
    wins_s: int = 0
    points_win_s: int = 0
    score_s: int = 0
    ach: List[int] = []
    achieves: List[str] = []
    assets: List[str] = []
    coll: dict = {}


class Achieve(Struct):
    id: str
    index: int
    mask: int
    level: int
    sort: int
    name: FormatLanguage
    desc: Optional[FormatLanguage] = None
    price: Optional[int] = None
    hidden: bool = False


class Achieves(Struct):
    items: List[Achieve]


class Smile(Struct):
    id: str
    index: int
    mask: int
    level: int
    name: FormatLanguage
    desc: Optional[FormatLanguage] = None
    price: Optional[int] = None
    hidden: bool = False
    group: Group = Group.EMPTY


class Frame(Struct):
    id: str
    index: int
    mask: int
    level: int
    name: FormatLanguage
    hidden: bool
    desc: Optional[FormatLanguage] = None
    price: Optional[int] = None
    group: Group = Group.EMPTY


class Shirt(Struct):
    id: str
    index: int
    mask: int
    level: int
    name: FormatLanguage
    hidden: bool = False
    desc: Optional[FormatLanguage] = None
    price: Optional[int] = None
    group: Group = Group.EMPTY


class Assets(Struct):
    smile: List[Smile]
    shirt: List[Shirt]


class ItemPrice(Struct):
    id: str
    name: dict
    price: int = None
    quantity: int = None
    money: int = None
    link: str = None


class ItemsPrice(Struct):
    ids: List[ItemPrice]


class PurchaseIds(Struct):
    ids: List


class Bets(Struct):
    v: List


class Game(Struct):
    id: int
    players: int
    position: int
    deck: int
    timeout: int
    sw: bool
    ch: bool
    dr: bool
    nb: bool
    bet: int
    fast: bool
    
    
class Message(Struct, rename={"_from": "from"}):
    id: int
    dtc: str
    _from: int
    to: int
    msg: str
    kind: Optional[str] = None
    payload: Optional[str] = None


class Conversation(Struct):
    id: int
    begin: bool
    users: dict
    data: List[Message]
    
class LeaderboardUser(Struct):
    user_id: int
    name: str
    dtp: str
    avatar: Optional[str]
    score: int
    count: int
    place: int
    pw: int
    frame: str
    achieve: str
    

class Leaderboard(Struct):
    type: str
    kind: str
    rows: List[LeaderboardUser]


class GameInList(Struct):
    id: int
    p: int
    cp: int
    bet: int
    name: str
    pr: bool
    nb: bool
    dr: bool
    sw: bool
    ch: bool
    fast: bool
