class UserListType(object):

    _banned = "banned"
    _banned_ip = "banned_ip"
    _opped = "opped"
    _whitelisted = "whitelisted"

    @property
    def Banned(self):
        return self._banned

    @property
    def BannedIP(self):
        return self._banned_ip

    @property
    def Opped(self):
        return self._opped

    @property
    def Whitelisted(self):
        return self._whitelisted
