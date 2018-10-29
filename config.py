import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    DEBUG = False
    type = "screen"
    session = "forge"
    whitelist = _basedir + '/data/whitelist.json'
    mc_root = "/srv/minecraft"


class DevConfig(Config):

    DEBUG = True




