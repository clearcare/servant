from decimal import Decimal

from schematics.types import (
        StringType,
        BooleanType,
        DateTimeType,
        DateType,
        DecimalType,
        EmailType,
        FloatType,
        GeoPointType,
        HashType,
        IPv4Type,
        IntType,
        LongType,
        MD5Type,
        NumberType,
        SHA1Type,
        StringType,
        URLType,
        UUIDType,
)
from schematics.types.compound import (
        DictType,
        ListType,
        ModelType,
)
from schematics.models import Model
# this one has another dependency...defer
#from schematics.types.temporal import (
#        TimeStampType as TimeStampField,
#)

TWOPLACES = Decimal('0.01')


class ServantFieldMixin(object):

    def __init__(self, *args, **kwargs):
        self.in_response = kwargs.pop('in_response', False)
        super(ServantFieldMixin, self).__init__(*args, **kwargs)

    def to_native(self, value, context=None):
        if value is None:
            return None
        return super(ServantFieldMixin, self).to_native(value, context)


class ServantCompoundFieldMixin(ServantFieldMixin):

    def __init__(self, field, **kwargs):
        if issubclass(field, ContainerField):
            field = ModelType(field)
        super(ServantCompoundFieldMixin, self).__init__(field, **kwargs)


# start special container fields

class ContainerField(ServantFieldMixin, Model):
    """Special type of field which is itself a model under the hood.

    This allows easy returning and validation of nested objects.

    """
    pass

class ListField(ServantCompoundFieldMixin, ListType):
    pass

class DictField(ServantCompoundFieldMixin, DictType):
    pass


# start standard fields

class ModelField(ServantFieldMixin, ModelType):
    pass


class BooleanField(ServantFieldMixin, BooleanType):
    pass

class DateTimeField(ServantFieldMixin, DateTimeType):
    pass

class DateField(ServantFieldMixin, DateType):
    pass

class DecimalField(ServantFieldMixin, DecimalType):
    pass

class EmailField(ServantFieldMixin, EmailType):
    pass

class FloatField(ServantFieldMixin, FloatType):
    pass

class GeoPointField(ServantFieldMixin, GeoPointType):
    pass

class HashField(ServantFieldMixin, HashType):
    pass

class IPv4Field(ServantFieldMixin, IPv4Type):
    pass

class IntField(ServantFieldMixin, IntType):
    pass

class LongField(ServantFieldMixin, LongType):
    pass

class MD5Field(ServantFieldMixin, MD5Type):
    pass

class NumberField(ServantFieldMixin, NumberType):
    pass

class SHA1Field(ServantFieldMixin, SHA1Type):
    pass

class StringField(ServantFieldMixin, StringType):
    pass

class URLField(ServantFieldMixin, URLType):
    pass

class UUIDField(ServantFieldMixin, UUIDType):
    pass

class CurrencyField(DecimalField):
    """Field which coerces value to two decimal places."""

    MESSAGES = {
        'number_coerce': 'Value failed to convert to a valid currency',
    }

    def to_native(self, value, context=None):
        value = super(CurrencyField, self).to_native(value, context=context)
        return value.quantize(TWOPLACES)
