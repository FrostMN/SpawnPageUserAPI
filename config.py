import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    DEBUG = False
    type = "screen"
    session = "forge"
    whitelist = _basedir + '/data/whitelist.json'


class DevConfig(Config):

    DEBUG = True




