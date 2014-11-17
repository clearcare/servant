class Service(object):
    name = 'base_service'
    version = 1

    def __init__(self):
        self._setup_actions()

    def _setup_actions(self):
        for name, actionclass in self.__class__.action_map.iteritems():
            setattr(self, name, actionclass())

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
