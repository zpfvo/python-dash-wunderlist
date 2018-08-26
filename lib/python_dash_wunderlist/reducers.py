from pydux.extend import extend
from python_dash_wunderlist.types import UPDATE_STATE


def reducer(state, action):
    if state is None:
        state = {
            'client_id': None,
            'client_secret': None,
            'dash_actions': {}
        }
    elif action['type'] == UPDATE_STATE:
        state = extend(state, action['payload'])
    return state
