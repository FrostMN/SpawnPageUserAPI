from abc import ABC
from abc import abstractmethod
from config import Config
import os


class CommandManager(ABC):

    @abstractmethod
    def op(self, user: str):
        pass

    @abstractmethod
    def deop(self, user: str):
        pass

    @abstractmethod
    def whitelist_add(self, user: str):
        pass

    @abstractmethod
    def whitelist_remove(self, user: str):
        pass

    @abstractmethod
    def ban(self, user: str):
        pass

    @abstractmethod
    def pardon(self, user: str):
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


# TODO: Actullay make this work it is all placeholders currently
class SystemdManager(CommandManager):

    session = ""
    cmd = "{}"

    def __init__(self, conf: Config):
        self.session = conf.session

    def op(self, user: str):
        op_cmd = "op {}".format(user)
        os.system(self.cmd.format(self.session, op_cmd))

    def deop(self, user: str):
        deop_cmd = "deop {}".format(user)

        print(deop_cmd)

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

    if config.type == "systemd":
        return ScreenManager(config)
