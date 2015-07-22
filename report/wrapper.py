
class ConfigurableWrapper(object):
    def __init__(self, cls):
        self._cls = cls

    def setup(self, *args, **kwargs):
        instance = self._cls(*args, **kwargs)
        self.__class__ = self._cls
        self.__dict__ = instance.__dict__
