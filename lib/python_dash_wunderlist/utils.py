def dhash(dict):
    return hash(frozenset(dict.items()))


def lmap(*args, **kwargs):
        return list(map(*args, **kwargs))


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item
