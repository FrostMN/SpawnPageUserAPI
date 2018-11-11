
class Auth(object):

    def api(self, func):

        def wrapper(*args, **kwargs):
            print("before route")
            func(*args, **kwargs)

        return wrapper()
