import json
import os
import ast
import time
from flask import make_response, request
from config import Config as conf
from typing import Union
from abc import ABC, abstractmethod
from SpawnPageUserAPI.utils.CommandManager import CommandManager, CommandManagerFactory
from SpawnPageUserAPI.enums.UserListType import UserListType
from config import Config


class UserListManager(ABC):

    user_list = list()
    command = CommandManager

    add_success = "{}"
    add_failure = "{}"
    add_exists = "{}"
    rem_success = "{}"
    rem_failure = "{}"
    rem_missing = "{}"

    def add(self, item: str):

        if not self._test_exists(item):

            if self._add(item):
                return {"error": False, "message": self.add_success.format(item)}
            else:
                return {"error": True, "message": self.add_failure.format(item)}
        else:
            return {"error": True, "message": self.add_exists.format(item)}

    def remove(self, item: str):

        if self._test_exists(item):

            if self._remove(item):
                return {"error": False, "message": self.rem_success.format(item)}
            else:
                return {"error": True, "message": self.rem_failure.format(item)}
        else:
            return {"error": True, "message": self.rem_missing.format(item)}

    def get(self, item: str=None):
        if item:
            return self._single_item(item=item)
        else:
            return UserListManager.jsonify(self.user_list)

    @abstractmethod
    def _single_item(self, item: str) -> [dict]:
        pass

    def _test_exists(self, item: str):
        for i in self.user_list:
            if i['name'].lower() == item.lower():
                return True
        return False

    # TODO: implement
    def _test_add(self, item: str) -> bool:

        return True

    # TODO: implement
    def _test_remove(self, item: str) -> bool:

        return True

    def _add(self, item: str):
        return self.command.add(user=item, cb=self._test_add)

    def _remove(self, item: str):
        return self.command.remove(user=item, cb=self._test_remove)

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

    # TODO: reevaluate
    @staticmethod
    # def unauthorized(self):
    def unauthorized():
        data = {"error": True, "message": "You are not authorized to perform this action."}
        return UserListManager.jsonify(data=data, status=401)


class OppedManager(UserListManager):

    add_success = "User '{}' was opped."
    add_failure = "There was an error opping '{}.'"
    add_exists = "User '{}' is already in the opped list."
    rem_success = "User '{}' was deopped."
    rem_failure = "There was an error deopping '{}.'"
    rem_missing = "User '{}' was not in the opped list."

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config, UserListType.Opped)
        self.path = os.path.join(config.mc_root, "ops.json")
        self.user_list = self.load_list(self.path)

    def _single_item(self, item: str):
        for u in self.user_list:
            if self.user_list:
                if "name" in u.keys():
                    if u['name'] == item:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])


class WhitelistManager(UserListManager):

    add_success = "User '{}' was added to the whitelist."
    add_failure = "There was an error adding '{}' to the whitelist."
    add_exists = "User '{}' is already in the whitelist."
    rem_success = "User '{}' was removed from the Whitelist."
    rem_failure = "There was an error adding '{}' to the Whitelist"
    rem_missing = "User '{}' was not in the Whitelist"

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config, UserListType.Whitelisted)
        self.path = os.path.join(config.mc_root, "whitelist.json")
        self.user_list = self.load_list(self.path)

    def _single_item(self, item: str):
        for u in self.user_list:
            if self.user_list:
                if "name" in u.keys():
                    if u['name'] == item:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])


class BannedPlayerManager(UserListManager):

    add_success = "User '{}' was banned."
    add_failure = "There was an error baning '{}'."
    add_exists = "User '{}' has already been banned."
    rem_success = "User '{}' was pardoned"
    rem_failure = "There was an error banning '{}'"
    rem_missing = "User '{}' was not in the banned list"

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config, UserListType.Banned)
        self.path = os.path.join(config.mc_root, "banned-players.json")
        self.user_list = self.load_list(self.path)

    def _single_item(self, item: str):
        for u in self.user_list:
            if self.user_list:
                if "name" in u.keys():
                    if u['name'] == item:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])


class BannedIPManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config, UserListType.BannedIP)
        self.path = os.path.join(config.mc_root, "banned-ips.json")
        self.user_list = self.load_list(self.path)

    def add(self, user: str):
        return {"error": "False", "message": "need to implement this."}

    def remove(self, user: str):
        return {"error": "False", "message": "need to implement this."}

    def _single_item(self, item: str):
        for u in self.user_list:
            if self.user_list:
                if "ip" in u.keys():
                    if u['ip'] == item:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])
