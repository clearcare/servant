from .base import Action

from servant.fields import DictField, StringField

class EchoAction(Action):

    stuff = DictField(StringField)

    @classmethod
    def pre_run(klass, **kwargs):
        return {'stuff': kwargs}

    def run(seld, **kwargs):
        return kwargs


class PingAction(Action):

    def run(self, **kwargs):
        return True
