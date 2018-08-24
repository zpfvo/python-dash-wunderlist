import logging
import sys

from python_dash_wunderlist import __version__


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s: %(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


class PythonDashWunderlist(object):

    def __init__(self, loglevel):
        setup_logging(loglevel)
        logging.info('PythonDashWunderlist {}'.format(__version__))
