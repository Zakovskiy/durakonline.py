import socket
import json
import requests
import threading
import random


class SocketListener:

    def __init__(self, client):
        self.client = client
        self.socket = None
        self.handlers = {}

    def create_connection(self, server_id: str = None, ip: str = None, port: int = None):
        """
        **Parametrs**
            - server_id ::
                "u0" - Diamond
                "u1" - Sapphire
                "u2" - Ruby
                "u3" - Emerald
                "u4" - Amethyst
                "u5" - Aquamarine
                "u6" - Topaz
                "u7" - Opal
                "u8" - Amber
                "u9" - Jade
                "uA" - Onyx
                "uB" - Lazurite
                "uC" - Pearls
                "uD" - Alexandrite
                None - random
        """
        if not ip:
            servers = self.get_servers()["user"]
            server = servers[server_id] if server_id else list(random.choice(list(servers.items())))[1]
            ip = server["host"]
            port = server["port"]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((ip, port))
        except Exception as e:
            if "error" in self.handlers:
                self.handlers["error"](e)
        threading.Thread(target=self.receive_messages).start()

    def send_server(self, data: dir):
        try:
            self.socket.send((data.pop('command')+json.dumps(data, separators=(',', ':')).replace("{}", '')+'\n').encode())
        except Exception as e:
            if "error" in self.handlers:
                self.handlers["error"](e)

    def get_servers(self):
        try:
            response = requests.get(f"{self.api_url}servers.json").json()
        except Exception as e:
            if "error" in self.handlers:
                self.handlers["error"](e)
        return response

    def event(self, command: str = "all"):
        def register_handler(handler):
            if command in self.handlers:
                self.handlers[command].append(handler)
            else:
                self.handlers[command] = [handler]
            return handler

        return register_handler

    def error(self):
        def register_handler(handler):
            self.handlers["error"] = handler
            return handler

        return register_handler

    def receive_messages(self):
        self.logger.debug(f"{self.tag}: Start listener")
        while True:
            buffer = bytes()
            while True:
                try:
                    r = self.socket.recv(4096)
                except Exception as e:
                    if "error" in self.handlers:
                        self.handlers["error"](e)
                        return
                buffer = buffer + r
                read = len(r)
                if read != -1:
                    if read in [0, 1]: continue
                    try:
                        d = buffer.decode()
                    except:
                        continue
                    if d.endswith('\n'):
                        buffer = bytes()
                        for str in d.strip().split('\n'):
                            str = str[0:-1]
                            pos = str.find('{')
                            command = str[:pos]
                            try:
                                message = json.loads(str[pos:]+"}")
                            except Exception as e:
                                continue
                            message['command'] = command
                            self.logger.debug(f"{self.tag}: {message}")
                            for handler_command in self.handlers:
                                if handler_command in ["all", command]:
                                    for handler in self.handlers[handler_command]:
                                        handler(message)
                            self.receive.append(message)
                    else:
                        continue
                else:
                    self.socket.close()
                    return

    def listen(self, force: bool = False):
        while len(self.receive) == 0:
            if force:
                return {"command": "empty"}
        r = self.receive[0]
        del self.receive[0]
        return r

    def _get_data(self, type, force: bool = False):
        data = self.listen(force=force)
        while 1:
            if data["command"] in [type, "err", "empty", "alert"]:
                return data
            data = self.listen(force=force)