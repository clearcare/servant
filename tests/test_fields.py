import pytest

import servant.fields
from servant.exceptions import ValidationError

def test_string_field():
    f = servant.fields.StringField(max_length=2)
    with pytest.raises(ValidationError):
        f.validate('abc')
