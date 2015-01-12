import importlib

from .base import BaseTransport


class LocalTransport(BaseTransport):

    def __init__(self):
        super(LocalTransport, self).__init__()
        self.__service = None

    def __repr__(self):
        return self.__class__.__name__

    def configure(self, service_name='', service_version='', service_meta=None):
        instance = self._import_service_and_instantiate_service(service_name, service_version)
        self.service = instance

    @property
    def service(self):
        raise AttributeError("Cannot access service property directly")

    @service.setter
    def service(self, service_instance):
        self.__service = service_instance

    def _import_service_and_instantiate_service(self, service_name, service_version):
        if not service_name and service_version:
            raise Exception(
                'service_name and service_version are required '
                'arguments for local transport')

        module = importlib.import_module('%s.service' % (service_name,))
        for name in dir(module):
            if name.startswith('_'):
                continue

            obj = getattr(module, name)
            if not self._looks_like_service_class(obj, service_name,
                    service_version):
                continue

            instance = obj()
            # uber-safe final check to make sure we have the correct service
            # class
            if not 'Service' in {b.__name__ for b in
                    instance.__class__.__bases__}:
                continue

            return instance

        raise Exception(
                'Could not find appropriate Service class. Services '
                'must subclass servant.Service and define an action_map, '
                'name and version.'
        )

    def _looks_like_service_class(self, obj, service_name, service_version):
        return (
                getattr(obj, 'name', '') == service_name and
                getattr(obj, 'version', -1) == service_version and
                isinstance(getattr(obj, 'action_map', None), dict) and
                hasattr(obj, 'run_actions')
        )

    def is_connected(self):
        return True

    def send(self, request):
        return self.__service.handle_request(request)

