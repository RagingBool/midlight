
def filter_for(geo_cls):
    """
    Factory of decorators, marking decorated function as a valid filter for
    given geometry class.
    """
    def deco(f):
        f._geo = geo_cls
        return f
    return deco


def is_filter_for(f, geo_cls):
    if not hasattr(f, "_geo"):
        return False
    if f._geo != geo_cls:
        return False
    return True
