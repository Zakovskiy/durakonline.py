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


class Server(str, Enum):
    DIAMOND = "u0"
    SAPPHIRE = "u1"
    RUBY = "u2"
    EMERALD = "u3"
    AMETHYST = "u4"
    AQUAMARINE = "u5"
    TOPAZ = "u6"
    OPAL = "u7"
    AMBER = "u8"
    JADE = "u9"
    ONYX = "uA"
    LAZURITE = "uB"
    PEARLS = "uC"
    ALEXANDRITE = "uD"
