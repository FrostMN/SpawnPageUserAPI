from abc import ABC, abstractmethod
from enum import Enum
import requests


class Urls(object):

    _profile = "https://sessionserver.mojang.com/session/minecraft/profile/"

    _usernames = "https://api.mojang.com/user/profiles/{uuid}/names"

    @property
    def profile(self):
        return self._profile

    @property
    def usernames(self):
        return self._usernames


class APIManager(ABC):
    pass


class MojangAPI(APIManager):

    urls = Urls()

    def profile(self, uuid: str):
        error = "False"

        call = self.urls.profile + uuid

        req = dict(requests.get(call).json())

        if "error" in req.keys():
            error = "True"
            payload = req
        else:
            payload = {"name": req['name'], "uuid": uuid}

        return {"error": error, "payload": payload}

    def username(self, uuid: str=None) -> str:
        if uuid:
            index = 0
            highest_index = 0
            highest = 0
            call = self.urls.usernames.format(uuid=uuid)
            try:
                req = requests.get(call).json()
            except:
                return False

            for name in req:
                if "changedToAt" in name.keys():
                    if int(name['changedToAt']) > highest:
                        highest = int(name['changedToAt'])
                        highest_index = index
                index += 1

            return req[highest_index]['name']
        return ""


if __name__ == '__main__':

    api = MojangAPI()

    # p = api.profile("f2c802de0196422fbe91b7b8bc078d03")
    # print(p)
    #
    p = api.username(uuid="f2c802de0196422fbe91b7b8bc078d03")
    print(p)

