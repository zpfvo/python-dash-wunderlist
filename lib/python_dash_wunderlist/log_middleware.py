from __future__ import print_function

from pprint import pformat


def log_middleware(store):
    """log all actions to console as they are dispatched"""
    def wrapper(next_):
        def log_dispatch(action):
            if action.get('loglevel') != 'DEBUG':
                print('Dispatch %s: %s' % (action['type'], pformat(action)))
            return next_(action)
        return log_dispatch
    return wrapper
