from pprint import pformat

import bunch

class ActionResult(object):

    def __init__(self, data):
        self._do_init(data)

    # {u'field_errors': None, u'errors': None, u'results': {u'stuff': {u'name':
    # u'bob'}}, u'action_name': u'echo'}
    def _do_init(self, data):
        self.__data = data
        self.__object = bunch.Bunch.fromDict(data)
        self.__action_result = self.__object.results

    def __getattr__(self, name):
        try:
            return getattr(self.__action_result, name)
        except AttributeError:
            raise AttributeError("'%s' object has no attribute '%s'" % (
                    self.__class__.__name__, name))

    @property
    def action_errors(self):
        """Return action-wide errors"""
        return self.__action_result.errors

    @property
    def field_errors(self):
        """Return specific field errors"""
        if not self.__action_result:
            raise AttributeError('Only single action responses can access field_errors from a response')
        return self.__action_result.field_errors



class Response(ActionResult):

    def _do_init(self, data):
        self.__data = data

        actions = data['actions']
        response_meta = data['response']

        self.__num_actions = len(actions)

        #self.__object = bunch.Bunch.fromDict(data)
        self.__meta = bunch.Bunch.fromDict(response_meta)

        self.__action_result = None
        self.__action_results = None

        if self.__num_actions == 1:
            self.__action_result = bunch.Bunch.fromDict(actions[0])
        else:
            self.__action_results = actions

    def __getattr__(self, name):
        try:
            if not self.__action_result:
                raise AttributeError
            return getattr(self.__action_result.results, name)
        except AttributeError:
            raise AttributeError("'%s' object has no attribute '%s'" % (
                    self.__class__.__name__, name))

    @property
    def meta(self):
        """Return meta data about the request/response"""
        return self.__meta

    @property
    def text(self):
        """Return the raw deserialized response as a formatted string"""
        return pformat(self.__data)

    @property
    def errors(self):
        """Return request-level errors"""
        return self.__meta.errors

    @property
    def action_errors(self):
        """Return action-wide errors"""
        if not self.__action_result:
            raise AttributeError('Only single action responses can access action_errors from a response')
        return self.__action_result.errors

    @property
    def field_errors(self):
        """Return specific field errors"""
        if not self.__action_result:
            raise AttributeError('Only single action responses can access field_errors from a response')
        return self.__action_result.field_errors

    def action_results(self):
        return self.__action_results.iteritems()

    def to_native(self):
        """Return the raw deserialized response as dict"""
        return self.__data

    def is_error(self):
        """Boolean whether there were any errors"""
        if self.__meta.errors:
            return True

#        for a in self.__meta.actions:
#            if a.errors or a.field_errors:
#                return True

        return False


class FutureResponse(Response):
    def __init__(self):
        pass

    def init_from_result(self, data):
        self._do_init(data)
