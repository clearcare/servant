import importlib
import sys

from functools import wraps

#from .base import Service
#from .actions.base import Action


def _nr_wrap_unexpected_error():
    """Wrap unexpected error handler of the Service"""
    def _nr_handle_unexpected_error(func, *args, **kwargs):

        @wraps(func)
        def wrapped(self, exc):
            newrelic.agent.record_exception(*sys.exc_info())
            return func(self, exc)

        return wrapped

    module = importlib.import_module('servant.service.base')
    Service = getattr(module, 'Service')
    Service.handle_unexpected_error = _nr_handle_unexpected_error(Service.handle_unexpected_error)


def _nr_wrap_action():
    """Wrap the base Action such that the transaction name in NR contains the action name"""
    def _nr_get_instance(func):
        # Since we're wrapping a classmethod there's a little bit more work involved..basically
        # unwrapping it first and rewrappint it later.
        unwrapped_func = func.__func__

        @wraps(unwrapped_func)
        def wrapped(action_klass, *args, **kwargs):
            # Transactions will end up named Python/Servant/Action/class_name in New Relic
            newrelic.agent.set_transaction_name(action_klass.__name__,
                    group='Python/Servant/Action')
            return unwrapped_func(action_klass, *args, **kwargs)

        return classmethod(wrapped)

    module = importlib.import_module('servant.service.actions')
    Action = getattr(module, 'Action')
    Action.get_instance = _nr_get_instance(Action.get_instance)


def wrap_for_new_relic():
    _nr_wrap_unexpected_error()
    _nr_wrap_action()


try:
    import newrelic.agent
    wrap_for_new_relic()
except ImportError:
    pass
