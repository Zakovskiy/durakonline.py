import socket
import socks
import json
import requests
import threading
import random

from durakonline.utils import Server


class SocketListener:
    def __init__(self, client, proxy: str = ""):
        self.client = client
        self.proxy = proxy
        self.alive = False
        self.api_url: str = "http://static.rstgames.com/durak/"
        self.socket = None
        self.handlers = {}

    def create_connection(self, server_id: Server = None, ip: str = None, port: int = None):
        if not ip:
            servers = self.get_servers()["user"]
            server = servers[server_id] if server_id else list(random.choice(list(servers.items())))[1]
            ip = server["host"]
            port = server["port"]
        if self.proxy:
            proxy_login, proxy_password, proxy_ip, proxy_port = self.proxy.replace("@", ":").split(":")

            socks.set_default_proxy(socks.SOCKS5, proxy_ip, int(proxy_port), username=proxy_login, password=proxy_password)
            socket.socket = socks.socksocket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.settimeout(10)
            self.socket.connect((ip, port))
        except Exception as e:
            if "error" in self.handlers:
                self.handlers["error"](e)
            return
        self.alive = True
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
            return
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
        while self.alive:
            buffer = bytes()
            while self.alive:
                try:
                    r = self.socket.recv(4096)
                except Exception as e:
                    if "error" in self.handlers:
                        self.handlers["error"](e)
                    self.alive = False
                    return
                buffer = buffer + r
                read = len(r)
                if read != -1:
                    if read < 2:
                        continue
                    try:
                        d = buffer.decode()
                    except:
                        continue
                    if d.endswith('\n'):
                        buffer = bytes()
                        for message_str in d.strip().split('\n'):
                            message_str = message_str[0:-1]
                            pos = message_str.find('{')
                            command = message_str[:pos]
                            try:
                                message = json.loads(message_str[pos:]+"}")
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
        while not self.receive:
            if force:
                return {"command": "empty"}
        response = self.receive[0]
        del self.receive[0]
        return response

    def _get_data(self, command: str, force: bool = False):
        data = self.listen(force=force)
        while True:
            if data["command"] in [command, "err", "empty", "alert"]:
                return data
            data = self.listen(force=force)
