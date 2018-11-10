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
        op_cmd = "op {}".format(user)
        os.system(self.cmd.format(self.session, op_cmd))

    def remove(self, user: str):
        deop_cmd = "deop {}".format(user)
        os.system(self.cmd.format(self.session, deop_cmd))


class ScreenWhitelistManager(ScreenManager):

    def add(self, user: str):
        wl_add = "whitelist add {}".format(user)
        os.system(self.cmd.format(self.session, wl_add))

    def remove(self, user: str):
        wl_rem = "whitelist remove {}".format(user)
        os.system(self.cmd.format(self.session, wl_rem))


class ScreenBannedManager(ScreenManager):

    def add(self, user: str, reason: str="Banned by an operator."):
        ban_cmd = "ban {user} {reason}".format(user=user, reason=reason)
        os.system(self.cmd.format(self.session, ban_cmd))

    def remove(self, user: str):
        par_cmd = "pardon {}".format(user)
        os.system(self.cmd.format(self.session, par_cmd))


class ScreenBannedIPManager(ScreenManager):

    def add(self, address: str):
        ban_cmd = "ban-ip {}".format(address)
        os.system(self.cmd.format(self.session, ban_cmd))

    def remove(self, address: str):
        par_cmd = "pardon-ip {}".format(address)
        os.system(self.cmd.format(self.session, par_cmd))


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
