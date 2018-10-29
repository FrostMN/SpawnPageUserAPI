from abc import ABC, abstractmethod
from enum import Enum
import requests


class Urls(object):

    _profile = "https://sessionserver.mojang.com/session/minecraft/profile/"

    @property
    def profile(self):
        return self._profile


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


api = MojangAPI()

p = api.profile("f2c802de0196422fbe91b7b8bc078d03")
print(p)

p = api.profile("f2c802de0196422fbe91b7b8bc078d03")
print(p)
