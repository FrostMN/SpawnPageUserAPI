import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    DEBUG = False
    TESTING = False
    USER_API_KEY = "user_api"

    type = "screen"
    # type = "subprocess"
    session = "forge"
    whitelist = _basedir + '/data/whitelist.json'
    mc_root = "/srv/minecraft"


class DevConfig(Config):

    DEBUG = True
    TESTING = False
    mc_root = os.path.join(_basedir, "data")


class StagingConfig(Config):

    DEBUG = True
    TESTING = False
    mc_root = "/srv/minecraft"


class LiveConfig(Config):

    DEBUG = False
    TESTING = False
    mc_root = "/srv/minecraft"


class TestConfig(Config):

    DEBUG = False
    TESTING = True
    mc_root = "/srv/minecraft"


def ConfigPicker(env: str):
    if env == 'LIVE':
        return LiveConfig
    if env == 'DEV':
        return DevConfig
    if env == 'STG':
        return StagingConfig
    if env == 'TEST':
        return TestConfig


del os