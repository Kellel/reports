
class ConfigurableWrapper(object):
    """
    This is a little trick I just made up.

    Allow a reference to the object you want to create to be created later all while referencing the object before hand

    This is mostly useful when creating web applications that need access to something like the db object, but the db object isn't configured until later in the application startup procedure.

    Basicly this object holds onto the reference to the cls you want to create and replaces itself with a class instance of the cls you specified once you have called setup
    """
    def __init__(self, cls):
        self._cls = cls

    def setup(self, *args, **kwargs):
        instance = self._cls(*args, **kwargs)
        self.__class__ = self._cls
        self.__dict__ = instance.__dict__
