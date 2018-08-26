from __future__ import print_function

from datetime import datetime, timedelta

from python_dash_wunderlist.types import RECEIVED_RAW_PACKET
from python_dash_wunderlist.utils import dhash

BUTTON_DEBOUNCE_TIME_DELTA = timedelta(seconds=10)


def dash_button_middleware(store):
    dispatch, get_state = store['dispatch'], store['get_state']
    action_timestamps = {}

    def wrapper(next_):
        def middleware_dispatcher(action):
            if action['type'] == RECEIVED_RAW_PACKET:
                button_src = action['src']
                dash_button_action = get_state().get(
                    'dash_actions', {}).get(
                        button_src)
                if dash_button_action:
                    action['loglevel'] = 'INFO'
                    now = datetime.now()
                    last_dispatch_time = action_timestamps.get(
                        dhash(dash_button_action),
                        now - BUTTON_DEBOUNCE_TIME_DELTA)
                    if now - BUTTON_DEBOUNCE_TIME_DELTA >= last_dispatch_time:
                        action_timestamps[dhash(dash_button_action)] = now
                        dispatch(dash_button_action)
            return next_(action)
        return middleware_dispatcher
    return wrapper
