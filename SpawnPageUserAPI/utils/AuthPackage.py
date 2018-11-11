
class Auth(object):

    def api(self, func):

        def wrapper():
            print("before route")
            func()

        return wrapper()