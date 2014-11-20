import json


class JsonSerializer(object):

    def serialize(self, data):
        return json.dumps(data)
