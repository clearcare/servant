from servant.client import Response


def test_not_error():
    d = {
        'actions': [ {'errors': None, 'field_errors': None} ],
        'response': {'errors': None},
    }
    resp = Response.fromDict(d)
    assert not resp.is_error()

def test_error_from_2nd_action():
    d = {
        'actions': [
            {'errors': None, 'field_errors': None},
            {'errors': 'Client error', 'field_errors': None},
        ],
        'response': {'errors': None},
    }
    resp = Response.fromDict(d)
    assert resp.is_error()

def test_error_from_2nd_action_field():
    d = {
        'actions': [
            {'errors': None, 'field_errors': None},
            {'errors': '', 'field_errors': {'input': 'error'}},
        ],
        'response': {'errors': None},
    }
    resp = Response.fromDict(d)
    assert resp.is_error()

def test_error_from_response():
    d = {
        'actions': [ {'errors': None, 'field_errors': None} ],
        'response': {'errors': 'There was an error'},
    }
    resp = Response.fromDict(d)
    assert resp.is_error()
