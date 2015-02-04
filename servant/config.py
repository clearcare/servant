import importlib
import os

from collections import MutableMapping


class Config(MutableMapping):

    def __init__(self, *args, **kwargs):
        self.__data = {}

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __delitem__(self, key):
        del self.__data[key]

    def __iter__(self):
        return iter(self.__data)

    def __len__(self):
        return len(self.__data)

    def __getattr__(self, name):
        try:
            return self.__data[name]
        except KeyError:
            raise AttributeError("%s object has no attribute '%s'" % (self.__class__.__name__, name))

    def from_envvar(self, variable_name):
        var = os.environ.get(variable_name)
        if not var:
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)
        return self.from_module(var)

    def from_module(self, module_name):
        """Updates the values in the config from a Python module.
        ``module_name`` must be on the system path and importable.

        :param module_name: the module_name of the config.

        """
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        self.from_object(module)
        return True

    def from_object(self, obj):
        """Updates the values from the given object.  An object can be of one
        of the following two types:

        -   a string: in this case the object with that name will be imported
        -   an actual object reference: that object is used directly

        Objects are usually either modules or classes.

        Just the uppercase variables in that object are stored in the config.
        Example usage::

            app.config.from_object('yourapplication.default_config')
            from yourapplication import default_config
            app.config.from_object(default_config)

        You should not use this function to load the actual configuration but
        rather configuration defaults.  The actual config should be loaded
        with :meth:`from_module` and ideally from a location not within the
        package because the package might be installed system wide.

        :param obj: an import name or object
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

