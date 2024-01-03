import json
from durakonline import durakonline

Durak = durakonline.Client()
Durak.authorization.signin_by_access_token("access_token")

@Durak.event(command="user_msg")
def event(data):
    user_id = data.get("from", Durak.uid)
    to = data["from"] if data["to"] == Durak.uid else data["to"]
    user_name = data["name"]
    Durak.send_message_friend(f">>{user_name}, hello!", to)
