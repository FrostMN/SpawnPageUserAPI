import json
import os
import ast
from flask import make_response, request
from config import Config as conf
from typing import Union
from abc import ABC, abstractmethod
from SpawnPageUserAPI.utils.CommandManager import CommandManager, CommandManagerFactory
from config import Config

# whitelist_path = conf.whitelist
#
#
# class UserListHandler(object):
#
#     user_list:  [dict]
#     path:       str
#
#     def __init__(self, file_path: str) -> None:
#         super().__init__()
#
#         with open(file_path) as json_file:
#             self.user_list = json.load(json_file)
#             self.path = file_path
#
#     def print(self):
#         for i in self.user_list:
#             print(i)
#
#     def _single_item(self, uuid: str):
#         for _single_item in self.user_list:
#             if _single_item["uuid"] == uuid:
#                 return _single_item
#         return {"message": "_single_item does not exist (needs to be rxpanded)"}
#
#     def add(self, _single_item: Union[dict, bytes]) -> dict:
#
#         if isinstance(_single_item, bytes):
#             _single_item = ast.literal_eval(_single_item.decode('utf-8'))
#
#         unique = True
#
#         if "uuid" in _single_item.keys():
#             for i in self.user_list:
#                 if "uuid" in i.keys():
#                     if i['uuid'] == _single_item["uuid"]:
#                         unique = False
#
#         if unique:
#             self.user_list.append(_single_item)
#             return {"message": "_single_item added (this should be expanded on)"}
#         return {"message": "_single_item already exists (this should be expanded on)"}
#
#     def remove(self, _single_item: Union[dict, bytes]) -> dict:
#
#         if isinstance(_single_item, bytes):
#             _single_item = ast.literal_eval(_single_item.decode('utf-8'))
#
#         unique = True
#         ind = 0
#
#         if "uuid" in _single_item.keys():
#             for index, i in enumerate(self.user_list):
#                 if "uuid" in i.keys():
#                     if i["uuid"] == _single_item["uuid"]:
#                         unique = False
#                         ind = index
#
#         if not unique:
#             self.user_list.pop(ind)
#             return {"message": "_single_item deleted from list (needs to be expanded)"}
#         return {"message": "_single_item not in list (needs to be expanded)"}
#
#     def save(self, path: str = None) -> None:
#         if path:
#             with open(path, "w") as json_file:
#                 json_file.write(json.dumps(self.user_list))
#         else:
#             with open(self.path, "w") as json_file:
#                 json_file.write(json.dumps(self.user_list))
#
#     def jsonify(self, uuid: str=None):
#
#         status = 200
#         indent = 4
#         sort_keys = True
#
#         if uuid:
#
#             _single_item = self._single_item(uuid)
#
#             response = make_response(json.dumps(_single_item, indent=indent, sort_keys=sort_keys))
#             response.headers['Content-Type'] = 'application/json; charset=utf-8'
#             response.headers['mimetype'] = 'application/json'
#             response.status_code = status
#             return response
#         else:
#
#             response = make_response(json.dumps(self.user_list, indent=indent, sort_keys=sort_keys))
#             response.headers['Content-Type'] = 'application/json; charset=utf-8'
#             response.headers['mimetype'] = 'application/json'
#             response.status_code = status
#             return response


class UserListManager(ABC):

    # command: CommandManager
    user_list = list()

    @abstractmethod
    def add(self, user: str):
        pass

    @abstractmethod
    def remove(self, user: str):
        pass

    # # @abstractmethod
    # def get(self):
    #     pass

    def get(self, item: str=None):
        if item:
            return UserListManager.jsonify(self._single_item(item=item))
        else:
            return UserListManager.jsonify(self.user_list)

    # @abstractmethod
    def _single_item(self, item: str):
        pass

    @staticmethod
    def jsonify(data, status: int=200, indent: int = 4, sort_keys: bool=True):

        response = make_response(json.dumps(data, indent=indent, sort_keys=sort_keys))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['mimetype'] = 'application/json'
        response.status_code = status
        return response


class OpedManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)
        self.path = os.path.join(config.mc_root, "ops.json")

        with open(self.path) as json_file:
            self.user_list = json.load(json_file)

    def add(self, user: str):
        self.command.op(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.deop(user)
        return {"error": "False", "message": "need to implement this message."}

    # def get(self):
    #     return UserListManager.jsonify(self.user_list)

    def _single_item(self, user: str):

        for u in self.user_list:

            print(u)

            if self.user_list:
                if "name" in u.keys():
                    if u['name'] == user:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])


class WhitelistManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)
        self.path = os.path.join(config.mc_root, "whitelist.json")

        with open(self.path) as json_file:
            print(self.path)
            print(json_file)
            self.user_list = json.load(json_file)

    def add(self, user: str):
        self.command.whitelist_add(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.whitelist_remove(user)
        return {"error": "False", "message": "need to implement this message."}

    def _single_item(self, user: str):

        for u in self.user_list:

            print(u)

            if self.user_list:
                if "name" in u.keys():
                    if u['name'] == user:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])


class BannedPlayerManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)
        self.path = os.path.join(config.mc_root, "banned-players.json")

        with open(self.path) as json_file:
            self.user_list = json.load(json_file)

    def add(self, user: str):
        self.command.ban(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.pardon(user)
        return {"error": "False", "message": "need to implement this message."}

    def _single_item(self, user: str):

        for u in self.user_list:

            print(u)

            if self.user_list:
                if "name" in u.keys():
                    if u['name'] == user:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])


class BannedIPManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)
        self.path = os.path.join(config.mc_root, "banned-ips.json")

        with open(self.path) as json_file:
            self.user_list = json.load(json_file)

    def add(self, user: str):
        self.command.ban_ip(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.pardon_ip(user)
        return {"error": "False", "message": "need to implement this message."}

    def _single_item(self, user: str):

        for u in self.user_list:

            print(u)

            if self.user_list:
                if "ip" in u.keys():
                    if u['ip'] == user:
                        return UserListManager.jsonify(data=[u])

        return UserListManager.jsonify(data=[])
