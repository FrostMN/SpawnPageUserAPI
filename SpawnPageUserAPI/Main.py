from flask import Flask, request
from SpawnPageUserAPI.utils.UserListManager import WhitelistManager, OpedManager, BanManager
from SpawnPageUserAPI.utils.MojangAPIManager import MojangAPI
import ast
import json

from config import DevConfig as conf

from SpawnPageUserAPI.application import app


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/v1/ping')
def pong():
    return '{ "message": "pong" }'


@app.route('/api/v1/whitelist', methods=["GET", "POST"])
def whitelist_usernames():

    whitelist = WhitelistManager(conf)

    # Adds user from post to white list
    if request.method == "POST":
        print(request.data)
        pass

    return ""


@app.route('/api/v1/whitelist/<uuid>', methods=["GET", "DELETE"])
def whitelist_user(uuid: str):

    whitelist = WhitelistManager(conf)

    # Adds user from post to white list
    if request.method == "DELETE":
        pass

    return ""


@app.route('/api/v1/admin', methods=["GET", "POST"])
def admin_usernames():

    oped = OpedManager(conf)
    req = ast.literal_eval(request.data.decode("utf-8"))

    # Adds user from post to white list
    if request.method == "POST":
        oped.add(req['username'])

    return ""


@app.route('/api/v1/admin/<uuid>', methods=["GET", "DELETE"])
def admin_user(uuid: str):

    message = ""
    whitelist = WhitelistManager(conf)
    mojang = MojangAPI()

    # Adds user from post to white list
    if request.method == "DELETE":

        profile = mojang.profile(uuid)
        message = whitelist.remove(profile['payload']['name'])

    return str(message)
