from enum import Enum


class Kind(Enum):
    EMPTY = ""
    FRIEND = "FRIEND"
    REQUEST = "REQUEST"
    INVITE = "INVITE"


class Group(Enum):
    EMPTY = ""
    SMILE = "smile"
    FRAME = "frame"
    SHIRT = "shirt"
    