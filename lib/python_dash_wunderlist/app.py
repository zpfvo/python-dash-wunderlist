import logging
import sys
from pprint import pformat, pprint

from pydux import apply_middleware, create_store
from python_dash_wunderlist import __version__
from python_dash_wunderlist.dash_button_middleware import \
    dash_button_middleware
from python_dash_wunderlist.log_middleware import log_middleware
from python_dash_wunderlist.reducers import reducer
from python_dash_wunderlist.sniffer_middleware import sniffer_middleware
from python_dash_wunderlist.types import ADD_WUNDERLIST_ENTRY, UPDATE_STATE
from python_dash_wunderlist.wunderlist_middleware import wunderlist_middleware
from twisted.internet import reactor

_logger = logging.getLogger(__name__)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s: %(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def diff_state_print_function(store):
    cl = {
        'old_state': None
    }

    def print_state():
        state = store.get_state()
        if state != cl['old_state']:
            print("STATE: %s" % pformat(state))
            cl['old_state'] = dict(state)
    return print_state


class PythonDashWunderlist(object):

    def __init__(self, loglevel, client_id, client_secret):
        setup_logging(loglevel)
        print('PythonDashWunderlist {}'.format(__version__))
        store = create_store(
            reducer,
            initial_state={
                'client_id': client_id,
                'client_secret': client_secret,
                'access_token': 'a4a548b2974997cfc7302ee8e6065c363a3c53bd5057a1a2e11ae56d237b',
                'dash_actions': {
                    '00:bb:3a:a0:e5:ac': {
                        'type': ADD_WUNDERLIST_ENTRY,
                        'list': 'WG Einkaufsliste',
                        'entry': 'Milch'
                    }}},
            enhancer=apply_middleware(
                sniffer_middleware,
                dash_button_middleware,
                wunderlist_middleware,
                log_middleware,
                ))

        store.subscribe(diff_state_print_function(store))
        reactor.run()
