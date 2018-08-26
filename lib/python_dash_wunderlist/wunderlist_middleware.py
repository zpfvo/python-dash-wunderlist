from __future__ import print_function

import wunderpy2
from python_dash_wunderlist.types import ADD_WUNDERLIST_ENTRY
from python_dash_wunderlist.utils import find, lmap

API = wunderpy2.WunderApi()


def wunderlist_middleware(store):
    """handle communication with wunderlist api"""
    get_state = store['get_state']

    client_id = get_state()['client_id']
    access_token = get_state()['access_token']
    client = API.get_client(access_token, client_id)
    wunderlist_ids = {}
    for item in client.get_lists():
        wunderlist_ids.update({item['title']: item['id']})
    print(wunderlist_ids)

    def wrapper(next_):
        def middleware_dispatcher(action):
            if action['type'] == ADD_WUNDERLIST_ENTRY:
                list_name = action['list']
                title = action['entry']
                list_id = wunderlist_ids[list_name]
                tasks = client.get_tasks(list_id)
                print(tasks)
                entry = find(lambda e: e['title'] == title, tasks)
                if entry:
                    client.update_task(
                        entry['id'], entry['revision'], starred=True)
                else:
                    client.create_task(list_id, title)
            return next_(action)
        return middleware_dispatcher
    return wrapper
