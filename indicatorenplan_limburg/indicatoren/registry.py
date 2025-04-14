_INDICATOR_REGISTRY = {}


def register_indicator(cls):
    _INDICATOR_REGISTRY[cls.__name__] = cls
    return cls


def get_registered_indicators():
    return _INDICATOR_REGISTRY.values()
