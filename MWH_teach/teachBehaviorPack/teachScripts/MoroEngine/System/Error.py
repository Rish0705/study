# coding=utf-8

# ================================================================================
# * Error
# --------------------------------------------------------------------------------
# - Version : 1.0.0
# - Last Update : 2021/04/15
# ================================================================================


class MoroEngineException(Exception):

    _msg = ""
    _dict = {}

    def __init__(self, **kwargs):
        self._dict = kwargs

    def _getDictMessage(self):
        return self._msg.format(**self._dict)

    def __str__(self):
        msg = self._getDictMessage()
        return msg


class InstanceError(MoroEngineException):

    _msg = "This is a static class. Can not get the instance of this class."

    def __init__(self, **kwargs):
        super(InstanceError, self).__init__(**kwargs)

    def __str__(self):
        return super(InstanceError, self).__str__()

