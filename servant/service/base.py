class Service(object):
    name = 'base_service'
    version = 1

    def __init__(self):
        pass

    def __getattr__(self, name):
        actionclass = self.__class__.action_map.get(name)
        if not actionclass:
            raise AttributeError
        return actionclass._do_run

    def describe(self):
        return u'%s, version %d' % (
                self.__class__.name,
                self.__class__.version)

    def get_client(self):
        return self

    def serialize(self):
        pass

    def deserialize(self):
        pass

    def validate(self):
        pass
