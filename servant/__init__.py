__version__ = '0.1.0'

# Fix a schematics py3.11 incompatibility
import collections
import collections.abc
collections.Iterable = collections.abc.Iterable

