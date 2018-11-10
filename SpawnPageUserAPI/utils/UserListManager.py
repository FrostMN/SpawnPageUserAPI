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

    def new_add(self, item: str):

        if not self._test_exists(item):

            if self._add(item):
                return {"error": False, "message": self.add_success.format(item)}
            else:
                return {"error": True, "message": self.add_failure.format(item)}
        else:
            return {"error": True, "message": self.add_exists.format(item)}

    @abstractmethod
    def remove(self, user: str):
        pass

    def new_remove(self, item: str):

        # exists = False

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
            print(item)
            if i['name'].lower() == item.lower():
                return True
        return False

    # TODO: implement
    def _test_add(self, item: str) -> bool:

        return True

        # new_list = self.load_list(self.path)
        #
        # for u in new_list:
        #     if u['name'].lower() == item.lower():
        #         return True
        # return False

    # TODO: implement
    def _test_remove(self, item: str) -> bool:
        return True

    def _add(self, item: str):
        return self.command.add(user=item, cb=self._test_add(item))

    def _remove(self, item: str):
        return self.command.remove(user=item, cb=self._test_remove(item))


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

    def remove(self, user: str):

        exists = False

        sucess_message = "User '{}' was deopped.".format(user)
        fail_message = "There was an error deopping '{}.'".format(user)
        not_in_list_message = "User '{}' was not opped.".format(user)

        for u in self.user_list:
            if u['name'].lower() == user.lower():
                self.command.remove(user)
                exists = True

        # This probably need to be improved
        time.sleep(3)
        new_list = self.load_list(self.path)

        if exists:
            if len(self.user_list) > len(new_list):
                return {"error": False, "message": sucess_message}
            else:
                message = "There was an error deopping '{}.'".format(user)
                return {"error": True, "message": fail_message}
        else:
            return {"error": True, "message": not_in_list_message}

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

    def remove(self, user: str):

        exists = False
        message = "User '{}' was not in whitelist.".format(user)

        for u in self.user_list:
            if u['name'].lower() == user.lower():
                self.command.remove(user)
                message = "User '{}' was removed from the whitelist.".format(str(u['name']))
                exists = True

        # This probably needs to be improved
        time.sleep(3)
        new_list = self.load_list(self.path)

        if exists:
            if len(self.user_list) > len(new_list):
                return {"error": False, "message": message}
            else:
                message = "There was an error removeing '{}' from the whitelist.".format(user)
                return {"error": True, "message": message}
        else:
            return {"error": True, "message": message}

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

    def remove(self, user: str):

        exists = False
        message = "User '{}' was not banned.".format(user)

        for u in self.user_list:
            if u['name'].lower() == user.lower():
                self.command.remove(user)
                message = "User '{}' was pardoned.".format(str(u['name']))
                exists = True

        # This probably needs to be improved
        time.sleep(3)
        new_list = self.load_list(self.path)

        if exists:
            if len(self.user_list) > len(new_list):
                return {"error": False, "message": message}
            else:
                message = "There was an error pardoning '{}.'".format(user)
                return {"error": True, "message": message}
        else:
            return {"error": True, "message": message}

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
