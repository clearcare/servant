from .base import Action

from servant.fields import (
        BooleanField,
        DictField,
        StringField,
)

class EchoAction(Action):

    stuff = DictField(
            StringField,
            in_response=True
    )

    @classmethod
    def pre_run(klass, **kwargs):
        return {'stuff': kwargs}

    def run(self, **kwargs):
        pass


class PingAction(Action):

    is_alive = BooleanField(
            in_response=True,
    )

    def run(self):
        try:
            self.is_alive = True
        except Exception:
            self.is_alive = False
