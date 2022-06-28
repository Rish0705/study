# coding=utf-8

# ================================================================================
# * Log
# --------------------------------------------------------------------------------
# - Version : 1.0.0
# - Last Update : 2021/04/27
# ================================================================================

# ================================================================================
# * Import
# --------------------------------------------------------------------------------
import logging
import sys
from ...MoroEngine.System.Error import InstanceError
# ================================================================================


class Log(object):
    _logger = None
    _handler = None

    def __init__(self):
        raise InstanceError()

    @classmethod
    def initialize(cls):
        cls.setLogger()
        cls.removeHandler()
        cls.addHandler()

    @classmethod
    def setLogger(cls):
        cls._logger = logging.getLogger('MoroEngine')
        cls._logger.propagate = False
        cls._logger.setLevel(logging.NOTSET)

    @classmethod
    def addHandler(cls):
        if not cls._logger.handlers:
            cls._handler = logging.StreamHandler(sys.stdout)
            fmt = "∨∨∨ %(levelname)s - File \"%(co_filename)s\", Line %(f_lineno)d, In %(co_name)s" \
                  "\n[%(asctime)s] >>> %(message)s"
            formatter = logging.Formatter(fmt, '%H:%M:%S')
            cls._handler.setFormatter(formatter)
            cls._logger.addHandler(cls._handler)

    @classmethod
    def removeHandler(cls):
        if cls._logger.handlers and cls._handler:
            cls._logger.removeHandler(cls._handler)
            cls._handler = None

    @classmethod
    def _getParameters(cls, frame):
        co_filename = frame.f_code.co_filename
        co_name = frame.f_code.co_name
        f_lineno = frame.f_lineno
        return {'co_filename': co_filename, 'co_name': co_name, 'f_lineno': f_lineno}

    @classmethod
    def Debug(cls, msg):
        cls._logger.debug(msg, extra=cls._getParameters(sys._getframe(1)))

    @classmethod
    def Info(cls, msg):
        cls._logger.info(msg, extra=cls._getParameters(sys._getframe(1)))

    @classmethod
    def Warn(cls, msg):
        cls.Warning(msg)

    @classmethod
    def Warning(cls, msg):
        cls._logger.warning(msg, extra=cls._getParameters(sys._getframe(1)))

    @classmethod
    def Error(cls, msg):
        cls._logger.error(msg, extra=cls._getParameters(sys._getframe(1)))

    @classmethod
    def Critical(cls, msg):
        cls._logger.critical(msg, extra=cls._getParameters(sys._getframe(1)))
