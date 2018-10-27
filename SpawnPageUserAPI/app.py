from flask import Flask, request
from SpawnPageUserAPI.utils.UserListHandler import UserListHandler
import json

from config import Config as conf

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/v1/ping')
def pong():
    return '{ "message": "pong" }'


@app.route('/api/v1/whitelist', methods=["GET", "POST"])
def whitelist_usernames():

    whitelist = UserListHandler(conf.whitelist)

    # Adds user from post to white list
    if request.method == "POST":

        message = whitelist.add(request.data)
        whitelist.save()

        print(message)

        return json.dumps(message)

    return whitelist.jsonify()


@app.route('/api/v1/whitelist/<uuid>', methods=["GET", "DELETE"])
def whitelist_user(uuid: str):

    whitelist = UserListHandler(conf.whitelist)

    # Adds user from post to white list
    if request.method == "DELETE":

        print(uuid)
        user = whitelist.get(uuid)
        print(user)
        message = whitelist.remove(user)
        whitelist.save()

        return json.dumps(message)

    return whitelist.jsonify(uuid)



if __name__ == '__main__':
    app.run()
