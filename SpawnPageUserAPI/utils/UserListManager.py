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
#     def user(self, uuid: str):
#         for user in self.user_list:
#             if user["uuid"] == uuid:
#                 return user
#         return {"message": "user does not exist (needs to be rxpanded)"}
#
#     def add(self, user: Union[dict, bytes]) -> dict:
#
#         if isinstance(user, bytes):
#             user = ast.literal_eval(user.decode('utf-8'))
#
#         unique = True
#
#         if "uuid" in user.keys():
#             for i in self.user_list:
#                 if "uuid" in i.keys():
#                     if i['uuid'] == user["uuid"]:
#                         unique = False
#
#         if unique:
#             self.user_list.append(user)
#             return {"message": "user added (this should be expanded on)"}
#         return {"message": "user already exists (this should be expanded on)"}
#
#     def remove(self, user: Union[dict, bytes]) -> dict:
#
#         if isinstance(user, bytes):
#             user = ast.literal_eval(user.decode('utf-8'))
#
#         unique = True
#         ind = 0
#
#         if "uuid" in user.keys():
#             for index, i in enumerate(self.user_list):
#                 if "uuid" in i.keys():
#                     if i["uuid"] == user["uuid"]:
#                         unique = False
#                         ind = index
#
#         if not unique:
#             self.user_list.pop(ind)
#             return {"message": "user deleted from list (needs to be expanded)"}
#         return {"message": "user not in list (needs to be expanded)"}
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
#             user = self.user(uuid)
#
#             response = make_response(json.dumps(user, indent=indent, sort_keys=sort_keys))
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

    @abstractmethod
    def add(self, user: str):
        pass

    @abstractmethod
    def remove(self, user: str):
        pass

    # @abstractmethod
    def user(self, user: str):
        pass

    @staticmethod
    def jsonify(data: dict, status: int=200, indent: int = 4, sort_keys: bool=True):

        response = make_response(json.dumps(data, indent=indent, sort_keys=sort_keys))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['mimetype'] = 'application/json'
        response.status_code = status
        return response


class OpedManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)
        self.mc_root = config.mc_root

    def add(self, user: str):
        self.command.op(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.deop(user)
        return {"error": "False", "message": "need to implement this message."}

    def user(self, user: str):

        print(user)

        file_path = os.path.join(self.mc_root, "ops.json")

        print(file_path)

        with open(file_path) as json_file:
            user_list = json.load(json_file)

            print(user_list)

            for u in user_list:

                print(u)

                if user_list:
                    if "name" in u.keys():
                        if u['name'] == user:
                            return UserListManager.jsonify(data=[u])
        return "[]"


class WhitelistManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)

    def add(self, user: str):
        self.command.whitelist_add(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.whitelist_remove(user)
        return {"error": "False", "message": "need to implement this message."}


class BanManager(UserListManager):

    def __init__(self, config: Config):
        self.command = CommandManagerFactory(config)

    def add(self, user: str):
        self.command.ban(user)
        return {"error": "False", "message": "need to implement this message."}

    def remove(self, user: str):
        self.command.pardon(user)
        return {"error": "False", "message": "need to implement this message."}
