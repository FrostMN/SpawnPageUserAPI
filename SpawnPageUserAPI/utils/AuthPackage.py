
class Auth(object):

    def api(self, route_funct):

        def wrapper():
            print("before route")
            route_funct()

        return wrapper()