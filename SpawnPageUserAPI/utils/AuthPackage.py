
class Auth(object):

    def api(self, func):

        def wrapper(*args, **kwargs):
            print("before route")
            func(*args, **kwargs)

        return wrapper()


def api(func):

    print("before def wr")

    def wrapper(*args, **kwargs):
        print("before route")
        func(*args, **kwargs)

    return wrapper()
