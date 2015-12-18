import pytest

from servant.service.base import Service


class Mixin(object):
    mixin = True

class ServiceV1(Service):
    version = 1
    name = 'test_service'
    action_map = {
            'foo': 'foo1',
            'bar': 'bar1',
    }

class ServiceV2(ServiceV1):
    version = 1
    action_map = {'foo': 'foo2'}

class ServiceV3(Mixin, ServiceV2):
    version = 1
    action_map = {
            'foo': 'foo3',
            'bar': 'bar3',
            'baz': 'baz3',
    }

class ServiceV4(Service):
    version = 1
    action_map = {
            'baz': 'baz4',
            'some_action': 555,
    }

class ServiceWithMultipleInheritence(ServiceV3, ServiceV4):
    version = 555



def test_version2():
    v2 = ServiceV2()
    assert v2.action_map == {
            'foo': 'foo2',
            'bar': 'bar1',
    }

def test_version3():
    v3 = ServiceV3()
    assert v3.action_map == {
            'foo': 'foo3',
            'bar': 'bar3',
            'baz': 'baz3',
    }
    assert v3.mixin is True

def test_multiple_inheritence():
    s = ServiceWithMultipleInheritence()
    assert s.version == 555
    assert s.action_map == {
            'foo': 'foo3',
            'bar': 'bar3',
            'baz': 'baz4',
            'some_action': 555,
    }

def test_missing_name():
    class NoName(Service):
        version = 1
        action_map = {}

    with pytest.raises(Exception):
        NoName()


def test_missing_version():
    class NoVersion(Service):
        name = 'service'
        action_map = {}

    with pytest.raises(Exception):
        NoName()


def test_missing_action_map():
    class NoActionMap(Service):
        name = 'service'
        version = 1

    s = NoActionMap()
    assert s.action_map == {}
