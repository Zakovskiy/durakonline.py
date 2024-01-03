import json
from .utils import objects
from msgspec.json import decode
from typing import List


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

    def get_list(self) -> List[objects.FriendInfo]:
        self.client.send_server(
            {
                "command": "friend_list"
            }
        )
        friends: List[objects.FriendInfo] = []
        data = self.client.listen()
        while data["command"] != "img_msg_price":
            if data["command"] == "fl_update":
                friends.append(decode(json.dumps(data), type=objects.FriendInfo))
            data = self.client.listen()

        return friends

    def send_message(self, content: str, to: int) -> objects.Message:
        self.client.send_server(
            {
                "command": "send_user_msg",
                "msg": content,
                "to": to
            }
        )
        response = self.client._get_data("user_msg")
        return decode(json.dumps(response), type=objects.Message)
        
    def delete_message(self, message_id: int) -> objects.Message:
        self.client.send_server(
            {
                "command": "delete_msg",
                "msg_id": message_id
            }
        )
        response = self.client._get_data("user_msg")
        return decode(json.dumps(response), type=objects.Message)
        
    def get_conversation(self, id: int) -> objects.Conversation:
        self.client.send_server(
            {
                "command": "get_conversation",
                "id": id
            }
        )
        response = self.client._get_data("conversation")
        return decode(json.dumps(response), type=objects.Conversation)
