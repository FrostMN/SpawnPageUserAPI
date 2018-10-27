from abc import ABC
from abc import abstractmethod
from config import Config
import os


class CommandManager(ABC):

    @abstractmethod
    def op(self):
        pass

    @abstractmethod
    def deop(self):
        pass

    @abstractmethod
    def whitelist_add(self):
        pass

    @abstractmethod
    def whitelist_remove(self):
        pass

    @abstractmethod
    def ban(self):
        pass

    @abstractmethod
    def pardon(self):
        pass


class ScreenManager(CommandManager):

    session = ""
    cmd = "screen -S {} -X stuff \"{}^M\""

    def __init__(self, conf: Config):
        self.session = conf.session

    def op(self, user: str):
        op_cmd = "op {}".format(user)
        os.system(self.cmd.format(self.session, op_cmd))

    def deop(self, user: str):
        deop_cmd = "deop {}".format(user)
        os.system(self.cmd.format(self.session, deop_cmd))

    def whitelist_add(self, user: str):
        wl_add = "whitelist add {}".format(user)
        os.system(self.cmd.format(self.session, wl_add))

    def whitelist_remove(self, user: str):
        wl_rem = "whitelist remove {}".format(user)
        os.system(self.cmd.format(self.session, wl_rem))

    def ban(self, user: str):
        ban_cmd = "ban {}".format(user)
        os.system(self.cmd.format(self.session, ban_cmd))

    def pardon(self, user: str):
        par_cmd = "pardon {}".format(user)
        os.system(self.cmd.format(self.session, par_cmd))


def CommandManagerFactory(config: Config) -> CommandManager:

    if config.type == "screen":
        return ScreenManager(config)