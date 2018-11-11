from config import ConfigPicker
import os
conf = ConfigPicker(os.environ['ENV'])

# # TODO: turn this into a proper @decorator
# class Auth(object):


def api(req):
    if 'Authorization' in req.keys() and \
            conf.USER_API_KEY == req['Authorization']:
        return True
    return False
