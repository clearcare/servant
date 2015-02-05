from pprint import pformat

import bunch


class Response(object):

    def __init__(self, data):
        self.__data = data
        self.__object = bunch.Bunch.fromDict(data)

        self.__num_actions = len(self.__object.actions)

        # for now.....one result
        self.__action_result = None
        if self.__num_actions > 0:
            self.__action_result = self.__object.actions[0]

        self.__meta = self.__object.response

    def __getattr__(self, name):
        try:
            return getattr(self.__action_result.results, name)
        except AttributeError:
            raise AttributeError("'%s' object has no attribute '%s'" % (
                    self.__class__.__name__, name))

    @classmethod
    def fromDict(klass, data):
        return klass(data)

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
        if not self.__meta.errors:
            return None
        return [e.error for e in self.__meta.errors]

    @property
    def full_errors(self):
        if not self.__meta.errors:
            return None
        return [e for e in self.__meta.errors]

    @property
    def action_errors(self):
        """Return action-wide errors"""
        if self.__action_result:
            return self.__action_result.errors

    @property
    def field_errors(self):
        """Return specific field errors"""
        if self.__action_result:
            return self.__action_result.field_errors

    def to_native(self):
        """Return the raw deserialized response as dict"""
        return self.__data

    def toDict(self):
        if self.__action_result.results:
            return self.__action_result.toDict()
        return None

    def is_error(self):
        """Boolean whether there were any errors"""
        if self.__object.response.errors:
            return True

        for a in self.__object.actions:
            if a.errors or a.field_errors:
                return True

        return False

