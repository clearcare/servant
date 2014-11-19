class TransportMixin(object):

    def get_transport(self):
        return self



class Service(TransportMixin):

    def __init__(self):
        if not hasattr(self, 'name'):
            raise Exception('Services must contain a name attribute')

        if not hasattr(self, 'version'):
            raise Exception('Services must contain a version attriute')

        for name, actionclass in self.__class__.action_map.iteritems():
            setattr(self, name, self.make_entry(actionclass))

    def make_entry(self, actionclass):
        def call_service(**kwargs):
            results = actionclass._do_run(**kwargs)
            return results

        return call_service

#    def __getattr__(self, name):
#        actionclass = self.__class__.action_map.get(name)
#        if not actionclass:
#            raise AttributeError("'%s' object has no attribute '%s'" % (
#                    self.__class__.__name__, name))
#
#        _do_run_method = getattr(actionclass, '_do_run')
#        if not _do_run_method or (
#                _do_run_method and not callable(_do_run_method)):
#            raise AttributeError("'%s' object has no attribute '%s'" % (
#                    self.__class__.__name__, name))
#
#        import pdb; pdb.set_trace()
#            #jaction_instance = actionclass()
#        return actionclass._do_run

    def describe(self):
        return u'%s, version %d' % (
                self.__class__.name,
                self.__class__.version)

    def get_client(self):
        return self.get_transport()


class HttpService(Service):
    pass
