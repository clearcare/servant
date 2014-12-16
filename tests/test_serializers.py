import pytest

from servant.serializers import JsonSerializer
from servant.service.actions import Action
from servant.utils import generate_cid

import servant.fields


class SubField(servant.fields.ContainerField):
    name = servant.fields.StringField()
    age = servant.fields.IntField()
    uuid = servant.fields.UUIDField()


class ParentAction(Action):
    parent_name = servant.fields.StringField()
    uuid = servant.fields.UUIDField()
    items = servant.fields.ListField(SubField)


@pytest.fixture
def json_serializer():
    return JsonSerializer()


@pytest.fixture
def parent_action():
    action = ParentAction({
        'parent_name': 'parent_action',
        'uuid': generate_cid(),
        'items': [SubField({'name': 'bz', 'age': 41, 'uuid': generate_cid()})],
    })
    return action


def test_serialize_deserialize_simple_obj(json_serializer):
    d = {'name': 'bz'}
    serialized = json_serializer.serialize(d)
    deserialized = json_serializer.deserialize(serialized)
    assert d == deserialized


def test_serialize_action(parent_action, json_serializer):
    assert json_serializer.serialize(parent_action)


def test_invalid_serialize(json_serializer):
    with pytest.raises(TypeError) as exc:
        json_serializer.serialize({'set': set((1, 2, 3))})
    assert 'is not JSON serializable' in str(exc.value)


def test_invalid_deserialize(json_serializer):
    with pytest.raises(TypeError) as exc:
        json_serializer.serialize({'set': set((1, 2, 3))})
    assert 'is not JSON serializable' in str(exc.value)


