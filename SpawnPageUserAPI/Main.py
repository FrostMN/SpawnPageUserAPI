from flask import Flask, request
from SpawnPageUserAPI.utils.UserListManager import WhitelistManager, OpedManager, BannedPlayerManager, BannedIPManager
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
def whitelist_users():

    whitelist = WhitelistManager(conf)

    # Adds Player from POST to whitelist.json
    if request.method == "POST":

        req = ast.literal_eval(request.data.decode("utf-8"))
        message = whitelist.add(req['username'])

        return message

    return whitelist.get()


@app.route('/api/v1/whitelist/<uuid>', methods=["GET", "DELETE"])
def whitelist_user(uuid: str):

    whitelist = WhitelistManager(conf)
    mojang = MojangAPI()

    uuid = uuid.replace("-", "")
    profile = mojang.profile(uuid)
    player = profile['payload']['name']

    # Removes Player in DELETE from whitelist.json
    if request.method == "DELETE":

        message = whitelist.remove(player)

        return message

    return whitelist.get(item=player)


@app.route('/api/v1/admin', methods=["GET", "POST"])
def admin_usernames():

    oped = OpedManager(conf)

    # Adds Player in POST to ops.json
    if request.method == "POST":
        req = ast.literal_eval(request.data.decode("utf-8"))
        oped.add(req['username'])

    return oped.get()


@app.route('/api/v1/admin/<uuid>', methods=["GET", "DELETE"])
def admin_user(uuid: str):

    opped = OpedManager(conf)
    mojang = MojangAPI()

    uuid = uuid.replace("-", "")
    profile = mojang.profile(uuid)
    player = profile['payload']['name']

    print(player)

    # Removes Player in DELETE from ops.json
    if request.method == "DELETE":

        message = opped.remove(player)

        return str(message)

    return opped.get(item=player)


@app.route('/api/v1/banned', methods=["GET", "POST"])
def banned_players():

    banned = BannedPlayerManager(conf)

    # Adds Player in POST to banned-players.json
    if request.method == "POST":
        req = ast.literal_eval(request.data.decode("utf-8"))
        banned.add(req['address'])

    return banned.get()


@app.route('/api/v1/banned/<uuid>', methods=["GET", "POST"])
def banned_player(uuid: str):

    uuid = uuid.replace("-", "")

    banned = BannedPlayerManager(conf)

    # removes Player in DELETE from banned-players.json
    if request.method == "DELETE":

        req = ast.literal_eval(request.data.decode("utf-8"))

        message = banned.remove(req['address'])
        return message

    return banned.get()


@app.route('/api/v1/addresses', methods=["GET", "POST"])
def banned_addresses():

    banned_ip = BannedIPManager(conf)

    # Adds IP in POST to banned-ips.json
    if request.method == "POST":
        req = ast.literal_eval(request.data.decode("utf-8"))
        banned_ip.add(req['address'])

    return banned_ip.get()


@app.route('/api/v1/addresses/<address>', methods=["GET", "POST"])
def banned_address(address: str):

    address = address.replace("-", ".")

    banned_ip = BannedIPManager(conf)

    # Removes IP in DELETE from banned-ips.json
    if request.method == "DELETE":

        req = ast.literal_eval(request.data.decode("utf-8"))

        message = banned_ip.remove(req['address'])
        return message

    return banned_ip.get()
