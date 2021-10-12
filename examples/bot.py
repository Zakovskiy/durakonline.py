import durakonline, json

Durak = durakonline.Client("access_token")

while dead:
	data = Durak.listen()

	type = data[0]
	content = data[1]
		

	if type == "user_msg":
		try:
			user_id = content["from"]
		except:
			user_id = 0
		to = content["from"] if content["to"] == Durak.uid else content["to"]
		user_name = content["name"]
		user_avatar = content["avatar"]
		content = content["msg"].lower()
		args = content.split()
		if (args[0] == "!id"):
			Durak.send_message_friend(f">>{user_name}, твой ID: {user_id}!", to)
		elif (args[0] == "!ava"):
			Durak.send_message_friend(f">>{user_name}, ваша аватарка - {user_avatar}", to)
		elif (args[0] == "!assetselect"):
			Durak.asset_select(args[1])
		elif (args[0] == "!getuser"):
			Durak.get_user_info(int(args[1]))