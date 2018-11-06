import json
import os
import ast
import time
from flask import make_response, request
from config import Config as conf
from typing import Union
from abc import ABC, abstractmethod
from SpawnPageUserAPI.utils.CommandManager import CommandManager, CommandManagerFactory
from config import Config


class UserListManager(ABC):

    # command: CommandManager
    user_list = list()

    path = ""

    @abstractmethod
    def add(self, user: str):
        pass

    @abstractmethod
    def remove(self, user: str):
        pass

    def get(self, item: str=None):
        if item:
            return self._single_item(item=item)
        else:
            return UserListManager.jsonify(self.user_list)

    @abstractmethod
    def _single_item(self, item: str) -> [dict]:
        pass

    @staticmethod
    def jsonify(data, status: int=200, indent: int = 4, sort_keys: bool=True):
        response = make_response(json.dumps(data, indent=indent, sort_keys=sort_keys))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['mimetype'] = 'application/json'
        response.status_code = status
        return response

    def load_list(self, path: str):
        with open(self.path) as json_file:
            return json.load(json_file)


class OpedManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)
        self.path = os.path.join(config.mc_root, "ops.json")
        self.user_list = self.load_list(self.path)

    def add(self, user: str):
        self.command.op(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.deop(user)
        return {"error": "False", "message": "need to implement this message."}

    def _single_item(self, item: str):
        for u in self.user_list:
            if self.user_list:
                if "name" in u.keys():
                    if u['name'] == item:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])


class WhitelistManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)
        self.path = os.path.join(config.mc_root, "whitelist.json")
        self.user_list = self.load_list(self.path)

    def add(self, user: str):

        for u in self.user_list:
            if u['name'].lower() == user.lower():
                message = "User '{}' is already in the whitelist.".format(str(u['name']))
                return {"error": False, "message": message, "user": u}
        self.command.whitelist_add(user)

        time.sleep(1)

        new_list = self.load_list(self.path)

        for u in new_list:
            if u['name'].lower() == user.lower():
                message = "User '{}' was added to the whitelist.".format(str(u['name']))
                return {"error": False, "message": message, "user": u}
        message = "There was an error adding {} to the whitelist. (this could be more robust)".format(user)
        return {"error": "True", "message": message}

    def remove(self, user: str):
        self.command.whitelist_remove(user)
        return {"error": "False", "message": "need to implement this message."}

    def _single_item(self, item: str):
        for u in self.user_list:
            if self.user_list:
                if "name" in u.keys():
                    if u['name'] == item:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])


class BannedPlayerManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)
        self.path = os.path.join(config.mc_root, "banned-players.json")
        self.user_list = self.load_list(self.path)

    def add(self, user: str):
        self.command.ban(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.pardon(user)
        return {"error": "False", "message": "need to implement this message."}

    def _single_item(self, item: str):
        for u in self.user_list:
            if self.user_list:
                if "name" in u.keys():
                    if u['name'] == item:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])


class BannedIPManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)
        self.path = os.path.join(config.mc_root, "banned-ips.json")
        self.user_list = self.load_list(self.path)

    def add(self, user: str):
        self.command.ban_ip(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.pardon_ip(user)
        return {"error": "False", "message": "need to implement this message."}

    def _single_item(self, item: str):
        for u in self.user_list:
            if self.user_list:
                if "ip" in u.keys():
                    if u['ip'] == item:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])
