from utils import objects
from datetime import datetime
from loguru import logger
import sys
import socket
import json
import threading
import bitstring
import base64
import hashlib

class Client:

	def __init__(self, token, pl:str="ios", debug:bool=False, language:str="ru"):
		self.pl = pl
		self.language = language
		self.uid = None
		self.receive = []
		self.create_connection()
		logger.remove()
		logger.add(sys.stderr, format="{time:HH:mm:ss.SSS}: {message}", level="DEBUG" if debug else "INFO")
		self.sign(self.get_session_key().key)
		if token:
			self.signin_by_access_token(token)

	def create_connection(self):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.settimeout(5000)
		self.client_socket.connect(('65.21.92.165', 10783))
		self.client_socket.settimeout(None)
		threading.Thread(target=self.receive_messages).start()

	def receive_messages(self):
		buffer = ""
		while True:
			try:
				data = self.client_socket.recv(4096).decode()
			except:
				continue
			buffer += data
			if not buffer.endswith('\n'):
				continue
			i1 = 0
			for i in buffer.split('\n'):
				i = i.replace('\n', '')
				pos = i.find('{')
				command = i[:pos]
				try:
					message = json.loads(i[pos:])
				except Exception:
					continue
				message['command'] = command
				logger.debug(message)
				self.receive.append(message)
			buffer = ""

	def send_server(self, data:dir):
		self.client_socket.send((data.pop('command')+json.dumps(data, separators=(',', ':')).replace("{}", '')+'\n').encode())

	def get_session_key(self):
		data = {
			"command":"c",
			"l":self.language,
			"tz":"+02:00",
			"t":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z",
			"pl":self.pl,
			"p":10
		}
		if self.pl == "iphone":
			data.update({
				"v":"1.9.1.2",
				"ios":"14.4",
				"d":"iPhone8,4",
				"n":"durak.ios"
			})
		else:
			data.update({
				"v":"1.9.2",
				"d":"xiaomi cactus",
				"and":28,
				"n":f"durak.{self.pl}"
			})
		self.send_server(
			data
		)
		return objects.GetSessionKey(self.listen()).GetSessionKey

	def sign(self, key):
		hash = base64.b64encode(hashlib.md5((key+"oc3q7ingf978mx457fgk4587fg847").encode()).digest()).decode()
		self.send_server(
			{
				"command":"sign",
				"hash":hash
			}
		)
		return self.listen()

	def signin_by_access_token(self, token):
		self.token = token
		self.send_server(
			{
				"command":"auth",
				"token":self.token
			}
		)
		authorized = self.listen()
		if authorized["command"] == "err":
			raise objects.Err(authorized)
		self.uid = authorized["id"]
		return self.uid

	def google_auth(self, id_token:str):
		self.send_server(
			{
				"command":"durak_google_auth",
				"id_token":id_token
			}
		)

	def get_captcha(self):
		self.send_server(
			{
				"command":"get_captcha"
			}
		)
		return self.__get_data("captcha")

	def register(self, name, captcha:str=''):
		self.send_server(
			{
				"command":"register",
				"name":name,
				"captcha":captcha
			}
		)
		data = self.listen()
		if data["command"] == "err": raise objects.Err(data)
		else: return objects.Register(data).Register

	def get_user_info(self, user_id:int):
		self.send_server(
			{
				"command":"get_user_info",
				"id":user_id
			}
		)
		data = self.__get_data("user_info")
		if data["command"] == "err": raise objects.Err(data)
		else: return objects.UserInfo(data).UserInfo

	def friend_accept(self, friend_id:int):
		self.send_server(
			{
				"command":"friend_accept",
				"id":friend_id
			}
		)

	def friend_delete(self, friend_id:int):
		self.send_server(
			{
				"command":"friend_delete",
				"id":friend_id
			}
		)

	def verify_purchase(self, signature, purchase_data):
		self.send_server(
			{
				"command":"verify_purchase",
				"signature":signature,
				"purchase_data":purchase_data
			}
		)

	def get_purchase_ids(self):
		self.send_server(
			{
				"command":"get_android_purchase_ids"
			}
		)
		return objects.PurchaseIds(self.__get_data("android_purchase_ids")).PurchaseIds

	def get_prem_price(self):
		self.send_server(
			{
				"command":"get_prem_price"
			}
		)
		return objects.ItemsPrice(self.__get_data("prem_price")).ItemsPrice

	def get_points_price(self):
		self.send_server(
			{
				"command":"get_points_price"
			}
		)
		return objects.ItemsPrice(self.__get_data("points_price")).ItemsPrice

	def buy_prem(self, id:int=0):
		self.send_server(
			{
				"command":"buy_prem",
				"id":f"com.rstgames.durak.prem.{id}"
			}
		)

	def buy_points(self, id:int=0):
		self.send_server(
			{
				"command":"buy_points",
				"id":f"com.rstgames.durak.points.{id}"
			}
		)

		return self.listen()

	def buy_asset(self, asset_id):
		self.send_server(
			{
				"command":"buy_asset",
				"id":asset_id
			}
		)

	def get_friend_list(self):
		self.send_server(
			{
				"command":"friend_list"
			}
		)
		friends = []
		data = self.listen()
		while data["command"] != "img_msg_price":
			friends.append(objects.FriendInfo(data).FriendInfo)
			data = self.listen()

		return friends

	def join_to_game(self, password:str, game_id):
		self.send_server(
			{
				"command":"join",
				"password":password,
				"id":game_id
			}
		)

	def rejoin_to_game(self, position, game_id):
		self.send_server(
			{
				"command":"rejoin",
				"p":position,
				"id":game_id
			}
		)

	def leave(self, game_id):
		self.send_server(
			{
				"command":"leave",
				"id":game_id
			}
		)

	def game_publish(self):
		self.send_server(
			{
				"command":"game_publish"
			}
		)

	def get_assets(self):
		self.send_server(
			{
				"command":"get_assets"
			}
		)
		return objects.Assets(self.__get_data("assets")).Assets

	def asset_select(self, asset_id):
		self.send_server(
			{
				"command":"asset_select",
				"id":asset
			}
		)

	def achieve_select(self, achieve_id):
		self.send_server(
			{
				"command":"achieve_select",
				"id":achieve_id
			}
		)

	def send_smile_game(self, smile_id:int=16):
		self.send_server(
			{
				"command":"smile",
				"id":smile_id
			}
		)

	def ready(self):
		self.send_server(
			{
				"command":"ready"
			}
		)

	def surrender(self):
		self.send_server(
			{
				"command":"surrender"
			}
		)

	def player_swap(self, position:int):
		self.send_server(
			{
				"command":"player_swap",
				"id":position
			}
		)

	def send_message_friend(self, content, to):
		self.send_server(
			{
				"command":"send_user_msg",
				"msg":content,
				"to":to
			}
		)

	def send_user_message_code(self, code, content):
		self.send_server(
			{
				"command":"send_user_msg_code",
				"code":code,
				"msg":content
			}
		)

	def delete_messege(self, messege_id):
		self.send_server(
			{
				"command":"delete_msg",
				"msg_id":messege_id
			}
		)

	def gift_coll_item(self, item_id:id, coll_id:str, to:int):
		self.send_server(
			{
				"command":"gift_coll_item",
				"item_id":item_id,
				"coll_id":coll_id,
				"to_id":to
			}
		)

	def get_bets(self):
		self.send_server(
			{
				"command":"gb"
			}
		)
		return objects.Bets(self.__get_data("bets")).Bets

	def create_game(self, bet, password:str="", players:int=3, deck:int=24, fast:bool=True):
		self.send_server(
			{
				"command":"create",
				"bet":bet,
				"password":password,
				"fast":fast,
				"sw":True,
				"nb":True,
				"ch":False,
				"players":players,
				"deck":deck,
				"dr":True
			}
		)

		data = self.__get_data("create")
		if data["command"] == 'err': raise objects.Err(data)
		else: return objects.Game(data).Game 

	def invite_to_game(self, user_id):
		self.send_server(
			{
				"command":"invite_to_game",
				"user_id":user_id
			}
		)

	def lookup_start(self, betMin:int=100, pr:bool=False, betMax:int=2500, fast:bool=True, sw:bool=True, nb:list=[False,True], ch:bool=False, players:list=[2,3,4,5,6], deck:list=[24,36,52], dr:bool=True):
		self.send_server(
			{
				"command":"lookup_start",
				"betMin":betMin,
				"pr":[pr, False],
				"betMax":betMax,
				"fast":[fast],
				"sw":[sw],
				"nb":nb,
				"ch":[ch],
				"players":players,
				"deck":deck,
				"dr":[dr],
				"status":"open"
			}
		)

	def lookup_stop(self):
		self.send_server(
			{
				"command":"lookup_stop"
			}
		)

	def get_server(self):
		self.send_server(
			{
				"command":"get_server"
			}
		)

	def update_name(self, nickname:str=None):
		self.send_server(
			{
				"command":"update_name",
				"value":nickname
			}
		)

	def save_note(self, note:str, user_id:int, color:int=0):
		self.send_server(
			{
				"command":"save_note",
				"note":note,
				"color":color,
				"id":user_id
			}
		)

	def leaderboard_get_by_user(self, user_id, type:str="score", season:bool=False):
		s = "" if not season else "s_"
		self.send_server(
			{
				"command":s+"lb_get_by_user",
				"user_id":user_id,
				"type":type
			}
		)

	def leaderboard_get_top(self, type:str="score"):
		self.send_server(
			{
				"command":"lb_get_top",
				"type":type
			}
		)

	def leaderboard_get_by_place_down(self, place:int=20, type:str="score"):
		self.send_server(
			{
				"command":"lb_get_by_place_down",
				"place":place,
				"type":type
			}
		)

	def turn(self, card):
		self.send_server(
			{
				"command":"t",
				"c":card
			}
		)

	def take(self):
		self.send_server(
			{
				"command":"take"
			}
		)

	def _pass(self):
		self.send_server(
			{
				"command":"pass"
			}
		)

	def listen(self):
		while len(self.receive) == 0:
			pass
		r = self.receive[0]
		del self.receive[0]
		return r

	def __get_data(self, type):
		data = self.listen()
		while 1:
			if data["command"] in [type,"err"]:
				return data
			data = self.listen()
