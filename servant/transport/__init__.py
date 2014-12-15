from .http import HttpTransport
from .local import LocalTransport


_TRANSPORT_MAPPING = {
        'http': HttpTransport(),
        'local': LocalTransport(),
}


def get_client_transport_class_by_name(name):
    return _TRANSPORT_MAPPING[name.lower()]

def get_server_transport_class_by_name(name):
    return _TRANSPORT_MAPPING[name.lower()]
