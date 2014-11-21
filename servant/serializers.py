import json

from .exceptions import SerializationError


class JsonSerializer(object):

    def serialize(self, data):
        return json.dumps(data)

    def deserialize(self, data):
        try:
            return json.loads(data)
        except ValueError, err:
            raise SerializationError(err.message)
