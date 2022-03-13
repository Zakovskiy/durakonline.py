class Err(Exception):

	def __init__ (self, data:dir):
		self.json = data
		try: self.code = data["code"]
		except: self.code = None

class GetSessionKey:

	def __init__ (self, data:dir):
		self.json = data
		self.key = None

	@property
	def GetSessionKey (self):
		self.key = self.json["key"]
		return self

class Server:

	def __init__ (self, data:dir):
		self.json = data
		self.time = None
		self.id = None

	@property
	def Server (self):
		self.time = self.json["time"]
		self.id = self.json["id"]
		return self

class SigninByAccessToken:

	def __init__ (self, data:dir):
		self.json = data
		self.id = None

	@property
	def SigninByAccessToken(self):
		self.id = self.json["id"]
		return self

class Register:

	def __init__ (self, data:dir):
		self.json = data
		self.token = None

	@property
	def Register(self):
		self.token = self.json["token"]
		return self

class User:

	def __init__ (self, data: dict):
		self.json = data
		self.id = None
		self.name = None
		self.avatar = None
		self.dtp = None
		self.frame = None
		self.score = None
		self.achieve = None
		self.pw = None

	@property
	def User(self):
		self.id = self.json["id"]
		self.name = self.json["name"]
		self.avatar = self.json["avatar"]
		self.dtp = self.json["dtp"]
		self.frame = self.json["frame"]
		self.score = self.json["score"]
		self.achieve = self.json["achieve"]
		self.pw = self.json["pw"]
		return self
	

class FriendInfo:

	def __init__ (self, data: dict):
		self.json = data
		self.user: User = None
		self.kind = None
		self.new = None

	@property
	def FriendInfo(self):
		self.kind = self.json.get("kind")
		self.new = self.json.get("new")
		self.user = User(self.json.get("user")).User
		return self
	

class UserInfo:

	def __init__ (self, data:dir):
		self.json = data
		self.id = None
		self.name = None
		self.avatar = None
		self.pw = None
		self.ach = []
		self.ach_c = None
		self.t_bronze = None
		self.t_silver = None
		self.t_gold = None
		self.wins = None
		self.wins_season = None
		self.points_win = None
		self.points_win_season = None
		self.score = None
		self.score_season = None
		self.dtp = None
		self.frame = None
		self.assets = []
		self.achieve = None
		self.achieves = []
		self.coll = {}

	@property
	def UserInfo(self):
		self.id = self.json["id"]
		self.name = self.json["name"]
		self.avatar = self.json["avatar"]
		self.pw = self.json["pw"]
		self.ach = self.json["ach"]
		self.ach_c = self.json["achc"]
		self.t_bronze = self.json["t_bronze"]
		self.t_silver = self.json["t_silver"]
		self.t_gold = self.json["t_gold"]
		self.wins = self.json["wins"]
		self.wins_season = self.json["wins_s"]
		self.points_win = self.json["points_win"]
		self.points_win_season = self.json["points_win_s"]
		self.score = self.json["score"]
		self.score_season = self.json["score_s"]
		self.dtp = self.json["dtp"]
		self.frame = self.json["frame"]
		self.assets = self.json["assets"]
		self.achieve = self.json["achieve"]
		self.achieves = self.json["achieves"]
		self.coll = self.json["coll"]
		return self

class Smile:

	def __init__ (self, data:dir):
		self.json = data
		self.id = None
		self.index = None
		self.mask = None
		self.level = None
		self.price = None
		self.name = None
		self.description = None

	@property
	def Smile(self):
		self.id = self.json["id"]
		self.index = self.json["index"]
		self.mask = self.json["mask"]
		self.level = self.json["level"]
		self.price = self.json["price"]
		self.name = self.json["name"]["ru"]
		self.description = self.json["desc"]["ru"]
		return self

class Frame:

	def __init__ (self, data:dir):
		self.json = data

	@property
	def Frame(self):
		return Shirt(self.json).Shirt


class Shirt:

	def __init__ (self, data:dir):
		self.json = data
		self.id = None
		self.index = None
		self.mask = None
		self.level = None
		self.price = None
		self.name = None
		self.description = None
		self.hidden = None
		self.group = None

	@property
	def Shirt(self):
		self.id = self.json["id"]
		self.index = self.json["index"]
		self.mask = self.json["mask"]
		self.level = self.json["level"]
		self.price = self.json["price"]
		self.name = self.json["name"]["ru"]
		try: self.description = self.json["desc"]["ru"]
		except: pass
		self.hidden = self.json["hidden"]
		self.group = self.json["group"]
		return self

class Assets:

	def __init__ (self, data:dir):
		self.json = data
		self.smile = []
		self.shirt = []

	@property
	def Assets (self):
		for smile in self.json["smile"]:
			self.smile.append(Smile(smile).Smile)
		return self

class ItemsPrice:

	def __init__ (self, data:dir):
		self.json = data
		self.ids = []

	@property
	def ItemsPrice(self):
		for id in self.json["ids"]:
			self.ids.append(ItemPrice(id).ItemPrice)
		return self

class PurchaseIds:

	def __init__ (self, data:dir):
		self.json = data
		self.ids = None

	@property
	def PurchaseIds(self):
		self.ids = self.json["ids"]
		return self

class Bets:

	def __init__ (self, data:dir):
		self.json = data
		self.v = []

	@property
	def Bets(self):
		self.v = self.json["v"]
		return self
	

class ItemPrice:

	def __init__(self, data:dir):
		self.json = data
		self.price = None
		self.quantity = None
		self.id = None

	@property
	def ItemPrice(self):
		self.price = self.json["price"]
		self.quantity = self.json["quantity"]
		self.id = self.json["id"]
		return self

class Game:

	def __init__ (self, data:dir):
		self.json = data
		self.id = None
		self.players = None
		self.position = None
		self.deck = None
		self.timeout = None
		self.sw = None
		self.ch = None
		self.dr = None
		self.nb = None
		self.bet = None
		self.fast = None

	@property
	def Game(self):
		self.id = self.json.get("id")
		self.players = self.json.get("players")
		self.position = self.json.get("position")
		self.deck = self.json.get("deck")
		self.timeout = self.json.get("timeout")
		self.sw = self.json.get("sw")
		self.ch = self.json.get("ch")
		self.dr = self.json.get("dr")
		self.nb = self.json.get("nb")
		self.bet = self.json.get("bet")
		self.fast = self.json.get("fast")
		return self