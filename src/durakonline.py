import socket, json, threading, bitstring

class Client:

	def __init__(self, token, p:int=11, device:str="xiaomi cactus", v:str="1.9.2", timezone:str="+03:00", _and:int=28, pl:str="android", language:str="ru", n:str="durak.android"):
		self.p = p
		self.device = device
		self.version = v
		self.timezone = timezone
		self._and = _and
		self.pl = pl
		self.language = language
		self.n = n
		self.receive = []
		self.create_connection()
		self.c()
		self.sign()
		self.signin_by_access_token(token)

	def create_connection(self):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		self.client_socket.settimeout(5000);
		self.client_socket.connect(('65.21.92.165', 10783));
		self.client_socket.settimeout(None);
		threading.Thread(target=self.receive_messages).start()

	def receive_messages(self):
		while True:
			byteBuffe = self.client_socket.recv(1042)
			byteBuffer = bitstring.BitStream()
			byteBuffer.append(byteBuffe)
			i = 0
			i2 = 0
			try:
				str = byteBuffer.bytes.decode("utf8")
			except:
				print("DEBUG<<EXCEPT")
				pass
			if (len(str) != 1 or not str.endswith("\n")):
				split = str.split("\n")
				if (len(split) != 1 or str.endswith("\n")):
					byteBuffer._setbytepos(0)
					while (True):
						i = len(split) if (str.endswith("\n")) else len(split) - 1
						if (i2 >= i):
							break
						if (len(split[i2]) > 0):
							print("DEBUG>>"+split[i2])
							self._split_on_command(split[i2])
						i2+=1
					if (len(split[len(split) - 1]) > 0 and not str.endswith("\n")):
						byteBuffer.append(split[len(split) - 1].encode("UTF-8"))
						continue
					continue
				continue
			byteBuffer._setbytepos(0)

	def _split_on_command(self, str:str):
		index = str.find("{")
		if (index != -1):
			try:
				bVar = json.loads(str[index:-1]+"}")
			except:
				bVar = {}
			str = str[0:index]
		else:
			bVar = {}
		if str == None:
			return
		self.receive.append([str, bVar])

	def c(self):
		self.send_server("c", {"p":self.p, "d":self.device, "v":self.version, "tz":self.timezone, "and":self._and, "pl":self.pl, "l":self.language, "n":self.n})
		return self.listen()

	def sign(self, hash:str="4TpfGINb08B+x1vAll3ghQ=="):
		self.send_server("sign", {"hash":hash})
		return self.listen()

	def signin_by_access_token(self, token):
		self.token = token
		self.send_server("auth", {"token":self.token})
		return self.listen()

	def __send_server(self, msg):
		msg += "\n";
		self.client_socket.send(msg.encode());

	def send_server(self, type, content:dir = None):
		if not content:
			self.__send_server(type)
		else:
			self.__send_server(type+json.dumps(content))

	def get_user_info(self, user_id:int):
		self.send_server("get_user_info", {"id":user_id});

	def friend_accept(self, friend_id:int):
		self.send_server("friend_accept", {"id":friend_id});

	def friend_delete(self, friend_id:int):
		self.send_server("friend_delete", {"id":friend_id})

	def buy_points(self, id:int=0):
		self.send_server("buy_points", {"id":f"com.rstgames.durak.points.{id}"})

	def buy_asset(self, asset_id):
		self.send_server("buy_asset", {"id":asset_id})

	def friend_list(self):
		self.send_server("friend_list")

	def join(self, password:str, game_id):
		self.send_server("join", {"password":password, "id":game_id})

	def rejoin(self, position, game_id):
		self.send_server("rejoin", {"p":position, "id":game_id})

	def leave(self, game_id):
		self.send_server("leave", {"id":game_id})

	def game_publish(self):
		self.send_server("game_publish")

	def get_assets(self):
		self.send_server("get_assets")

	def asset_select(self, asset_id):
		self.send_server("asset_select", {"id":asset})

	def achieve_select(self, achieve_id):
		self.send_server("achieve_select", {"id":achieve})

	def send_smile_game(self, smile_id:int=16):
		self.send_server("smile", {"id":smile_id})

	def ready(self):
		self.send_server("ready")

	def surrender(self):
		self.send_server("surrender")

	def player_swap(self, position):
		self.send_server("player_swap", {"id":position})

	def send_message_friend(self, content, to):
		self.send_server("send_user_msg", {"msg":content, "to":to})

	def send_user_message_code(self, code, content):
		self.send_server("send_user_msg_code", {"code":code, "msg":content})

	def delete_messege(self, messege_id):
		self.send_server("delete_msg", {"msg_id":messege_id})

	def gift_coll_item(self, item_id:id, coll_id:str, to:int):
		self.send_server("gift_coll_item", {"item_id":item_id, "coll_id":coll_id,"to_id":to})

	def create_game(self, bet, password, players:int=3, deck:int=24, fast:bool=True):
		self.send_server("create", {"bet":bet,"password":password,"fast":fast,"sw":True,"nb":True,"ch":False,"players":players,"deck":deck,"dr":True});

	def invite_to_game(self, user_id):
		self.send_server("invite_to_game", {"user_id":user_id})

	def lookup_start(self, betMin:int=100, pr:bool=False, betMax:int=2500, fast:bool=True, sw:bool=True, nb:list=[False,True], ch:bool=False, players:list=[2,3,4,5,6], deck:list=[24,36,52], dr:bool=True):
		self.send_server("lookup_start", {"betMin":betMin, "pr":[pr, False], "betMax":betMax, "fast":[fast], "sw":[sw], "nb":nb, "ch":[ch], "players":players, "deck":deck, "dr":[dr], "status":"open"})

	def lookup_stop(self):
		self.send_server("lookup_stop")

	def get_server(self):
		self.send_server("get_server")

	def update_name(self, nickname:str=None):
		self.send_server("update_name", {"value":nickname})

	def save_note(self, note:str, user_id:int, color:int=0):
		self.send_server("save_note", {"note":note, "color":color, "id":user_id})

	def leaderboard_get_by_user(self, user_id, type:str="score", season:bool=False):
		s = "" if not season else "s_"
		self.send_server(s+"lb_get_by_user", {"user_id":user_id, "type":type})

	def leaderboard_get_top(self, type:str="score"):
		self.send_server("lb_get_top", {"type":type})

	def leaderboard_get_by_place_down(self, place:int=20, type:str="score"):
		self.send_server("lb_get_by_place_down", {"place":place, "type":type})

	def listen(self):
		while (len(self.receive) == 0):
			pass;
		r = self.receive[0]
		del self.receive[0]
		return [r[0], r[1]]