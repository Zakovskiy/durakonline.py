from .utils import objects


class Friend:

    def __init__(self, client) -> None:
        self.client = client

    def accept(self, friend_id: int) -> None:
        self.client.send_server(
            {
                "command": "friend_accept",
                "id": friend_id
            }
        )

    def delete(self, friend_id: int) -> dict:
        self.client.send_server(
            {
                "command": "friend_delete",
                "id": friend_id
            }
        )
        return self.client._get_data("fl_delete")

    def send_request(self, user_id: int) -> dict:
        self.client.send_server(
            {
                "command": "friend_request",
                "id": user_id
            }
        )
        return self.client.listen()

    def get_list(self) -> [objects.FriendInfo]:
        self.client.send_server(
            {
                "command": "friend_list"
            }
        )
        friends: [objects.FriendInfo] = []
        data = self.client.listen()
        while data["command"] != "img_msg_price":
            if data["command"] == "fl_update":
                friends.append(objects.FriendInfo(data).FriendInfo)
            data = self.client.listen()

        return friends

    def send_message(self, content, to) -> None:
        self.client.send_server(
            {
                "command": "send_user_msg",
                "msg": content,
                "to": to
            }
        )
