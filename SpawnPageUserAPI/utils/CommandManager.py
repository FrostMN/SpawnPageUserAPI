from abc import ABC
from abc import abstractmethod
from SpawnPageUserAPI.enums.UserListType import UserListType
from config import Config
import time
import os


class CommandManager(ABC):

    @abstractmethod
    def add(self, user: str, cb=None, wait: int=1):
        pass

    @abstractmethod
    def remove(self, user: str, cb=None, wait: int=1):
        pass


class ScreenManager(CommandManager):

    cmd = "screen -S {} -X stuff \"{}^M\""

    def __init__(self, conf: Config):
        self.session = conf.session


class ScreenAdminManager(ScreenManager):

    def add(self, user: str, cb=None, wait: int=1):
        op_cmd = "op {}".format(user)
        os.system(self.cmd.format(self.session, op_cmd))
        if cb:
            time.sleep(wait)
            return cb(user)

    def remove(self, user: str, cb=None, wait: int=1):
        deop_cmd = "deop {}".format(user)
        os.system(self.cmd.format(self.session, deop_cmd))
        if cb:
            time.sleep(wait)
            return cb(user)
1

class ScreenWhitelistManager(ScreenManager):

    def add(self, user: str, cb=None, wait: int=1):
        wl_add = "whitelist add {}".format(user)
        os.system(self.cmd.format(self.session, wl_add))
        if cb:
            time.sleep(wait)
            return cb(user)

    def remove(self, user: str, cb=None, wait: int=1):
        wl_rem = "whitelist remove {}".format(user)
        os.system(self.cmd.format(self.session, wl_rem))
        if cb:
            time.sleep(wait)
            return cb(user)


class ScreenBannedManager(ScreenManager):

    def add(self, user: str, reason: str="Banned by an operator.", cb=None, wait: int=1):
        ban_cmd = "ban {user} {reason}".format(user=user, reason=reason)
        os.system(self.cmd.format(self.session, ban_cmd))
        if cb:
            time.sleep(wait)
            return cb(user)

    def remove(self, user: str, cb=None, wait: int=1):
        par_cmd = "pardon {}".format(user)
        os.system(self.cmd.format(self.session, par_cmd))
        if cb:
            time.sleep(wait)
            return cb(user)


class ScreenBannedIPManager(ScreenManager):

    def add(self, address: str, cb=None, wait: int=1):
        ban_cmd = "ban-ip {}".format(address)
        os.system(self.cmd.format(self.session, ban_cmd))
        if cb:
            time.sleep(wait)
            return cb(address)

    def remove(self, address: str, cb=None, wait: int=1):
        par_cmd = "pardon-ip {}".format(address)
        os.system(self.cmd.format(self.session, par_cmd))
        if cb:
            time.sleep(wait)
            return cb(address)


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
