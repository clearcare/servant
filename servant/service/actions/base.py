from schematics.models import Model
from schematics.exceptions import ModelValidationError


class ActionResponse(object):

    def __init__(self, data, **kwargs):
        self.data = data


class Action(Model):

#    def __call__(self, **kwargs):
#        if self.is_valid():
#            return self.run(**kwargs)
#        return self.handle_errors(**kwargs)

    @classmethod
    def _do_run(klass, **kwargs):
        kwargs = klass.pre_run(**kwargs)
        instance = klass(raw_data=kwargs)
        action_results = instance.run(**kwargs)
        return ActionResponse(action_results).data

    @classmethod
    def pre_run(klass, **kwargs):
        return kwargs

    def run(self, **kwargs):
        raise NotImplementedError('Clients must implement this metho')

    def is_valid(self):
        try:
            self.validate()
            return True
        except ModelValidationError:
            return False

    def handle_errors(self, **kwargs):
        return 'error'
