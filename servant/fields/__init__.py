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
# this one has another dependency...defer
#from schematics.types.temporal import (
#        TimeStampType as TimeStampField,
#)


class ServantFieldMixin(object):

    def __init__(self, *args, **kwargs):
        self.in_response = kwargs.pop('in_response', False)
        super(ServantFieldMixin, self).__init__(*args, **kwargs)


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

class DictField(ServantFieldMixin, DictType):
    pass

class ListField(ServantFieldMixin, ListType):
    pass

class ModelField(ServantFieldMixin, ModelType):
    pass
