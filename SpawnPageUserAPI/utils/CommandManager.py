from abc import ABC
from abc import abstractmethod
from SpawnPageUserAPI.enums.UserListType import UserListType
from config import Config
import os


class CommandManager(ABC):

    @abstractmethod
    def add(self, usr: str):
        pass

    @abstractmethod
    def remove(self, usr: str):
        pass


class ScreenManager(CommandManager):

    cmd = "screen -S {} -X stuff \"{}^M\""

    def __init__(self, conf: Config):
        self.session = conf.session

    @abstractmethod
    def add(self, usr: str):
        pass

    @abstractmethod
    def remove(self, usr: str):
        pass


class ScreenAdminManager(ScreenManager):

    def add(self, user: str):
        print("op")
        op_cmd = "op {}".format(user)
        print(op_cmd)
        os.system(self.cmd.format(self.session, op_cmd))

    def remove(self, user: str):
        print("deop")
        deop_cmd = "deop {}".format(user)
        os.system(self.cmd.format(self.session, deop_cmd))


class ScreenWhitelistManager(ScreenManager):

    def add(self, user: str):
        print("wl_add")
        wl_add = "whitelist add {}".format(user)
        os.system(self.cmd.format(self.session, wl_add))

    def remove(self, user: str):
        print("wl_remove")
        wl_rem = "whitelist remove {}".format(user)
        os.system(self.cmd.format(self.session, wl_rem))


class ScreenBannedManager(ScreenManager):

    def add(self, user: str, reason: str="Banned by an operator."):
        print("ban")
        ban_cmd = "ban {user} {reason}".format(user=user, reason=reason)
        os.system(self.cmd.format(self.session, ban_cmd))

    def remove(self, user: str):
        print("pardon")
        par_cmd = "pardon {}".format(user)
        os.system(self.cmd.format(self.session, par_cmd))


class ScreenBannedIPManager(ScreenManager):

    def add(self, address: str):
        ban_cmd = "ban-ip {}".format(address)
        os.system(self.cmd.format(self.session, ban_cmd))

    def remove(self, address: str):
        par_cmd = "pardon-ip {}".format(address)
        os.system(self.cmd.format(self.session, par_cmd))


# class CommandIF(object):
#
#     def __init__(self, config: Config, command: CommandManager, list_type: str):
#         self.config = config
#         self.command = command
#
#         print("list_type")
#         print(list_type)
#
#         if list_type == "op":
#             print("CIF op")
#             self.add = self.command.op
#             self.remove = self.command.deop
#         if list_type == "wl":
#             print("CIF wl")
#             self.add = self.command.whitelist_add
#             self.remove = self.command.whitelist_remove
#         if list_type == "ban":
#             print("CIF ban")
#             self.add = self.command.ban
#             self.remove = self.command.pardon
#         if list_type == "ip":
#             print("CIF ip")
#             self.add = self.command.ban_ip
#             self.remove = self.command.pardon_ip
#
#         self.add = command.ban
#
#     def add(self, item: str):
#         self.add(item)
#
#     def remove(self, item:str):
#         self.remove(item)
#
#
# def ScreenManagerFactory():
#     pass


# TODO: Change list_type to enumeration
def CommandManagerFactory(config: Config, user_list_type: str) -> CommandManager:

    if config.type == "screen":
        if user_list_type == UserListType.Opped:
            return ScreenAdminManager(config)
        if user_list_type == UserListType.Banned:
            return ScreenBannedManager(config)
        if user_list_type == UserListType.Whitelisted:
            return ScreenWhitelistManager(config)
        if user_list_type == UserListType.BannedIP:
            return ScreenBannedIPManager(config)
