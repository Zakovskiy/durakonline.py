import durakonline, json

Durak = durakonline.Client("access_token")

@Durak.event(command="user_msg")
def event(data):
    try:
        user_id = data["from"]
    except:
        user_id = Durak.uid
    to = data["from"] if data["to"] == Durak.uid else data["to"]
    user_name = data["name"]
    Durak.send_message_friend(f">>{user_name}, hello!", to)
