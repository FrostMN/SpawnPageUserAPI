from flask import Flask, request
from SpawnPageUserAPI.utils.UserListManager import WhitelistManager, OppedManager, BannedPlayerManager, BannedIPManager, UserListManager
from SpawnPageUserAPI.utils.MojangAPIManager import MojangAPI
import ast
from SpawnPageUserAPI.application import app
from SpawnPageUserAPI.application import conf

# import os
# import json
# from config import ConfigPicker
# conf = ConfigPicker(os.environ['ENV'])


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test')
def test():

    print(request.headers['Authorization'])

    return 'Hello World!'


@app.route('/api/v1/ping')
def pong():
    return '{ "message": "pong" }'


@app.route('/api/v1/whitelist', methods=["GET", "POST"])
def whitelist_users():

    whitelist = WhitelistManager(conf)

    # Adds Player from POST to whitelist.json
    if request.method == "POST":

        key = request.headers
        print(key)

        req = ast.literal_eval(request.data.decode("utf-8"))

        message = whitelist.add(req['username'])

        return UserListManager.jsonify(message)

    return whitelist.get()


@app.route('/api/v1/whitelist/<uuid>', methods=["GET", "DELETE"])
def whitelist_user(uuid: str):

    whitelist = WhitelistManager(conf)
    mojang = MojangAPI()

    uuid = uuid.replace("-", "")
    player = mojang.username(uuid=uuid)

    # Removes Player in DELETE from whitelist.json
    if request.method == "DELETE":

        message = whitelist.remove(player)

        return UserListManager.jsonify(message)

    return whitelist.get(item=player)


@app.route('/api/v1/admin', methods=["GET", "POST"])
def admin_usernames():

    # create OppedManager
    opped = OppedManager(conf)

    # Adds Player in POST to ops.json
    if request.method == "POST":
        req = ast.literal_eval(request.data.decode("utf-8"))
        message = opped.add(req['username'])

        return UserListManager.jsonify(message)

    return opped.get()


@app.route('/api/v1/admin/<uuid>', methods=["GET", "DELETE"])
def admin_user(uuid: str):

    opped = OppedManager(conf)
    mojang = MojangAPI()

    uuid = uuid.replace("-", "")
    player = mojang.username(uuid=uuid)

    # Removes Player in DELETE from ops.json
    if request.method == "DELETE":

        message = opped.remove(player)

        return UserListManager.jsonify(message)

    return opped.get(item=player)


@app.route('/api/v1/banned', methods=["GET", "POST"])
def banned_players():

    banned = BannedPlayerManager(conf)

    # Adds Player in POST to banned-players.json
    if request.method == "POST":
        req = ast.literal_eval(request.data.decode("utf-8"))
        message = banned.add(req['username'])

        return UserListManager.jsonify(message)

    return banned.get()


@app.route('/api/v1/banned/<uuid>', methods=["GET", "DELETE"])
def banned_player(uuid: str):
    banned = BannedPlayerManager(conf)
    mojang = MojangAPI()

    uuid = uuid.replace("-", "")
    player = mojang.username(uuid=uuid)

    # removes Player in DELETE from banned-players.json
    if request.method == "DELETE":

        message = banned.remove(player)

        return UserListManager.jsonify(message)

    return banned.get(item=player)


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

        return UserListManager.jsonify(message)

    return banned_ip.get()
