from .base import Action

class EchoAction(Action):

    def run(self, **kwargs):
        return kwargs


class PingAction(Action):

    def run(self, **kwargs):
        return True
