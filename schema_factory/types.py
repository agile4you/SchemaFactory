# -*- coding: utf-8 -*-
"""`schema_factory.node_types` module.

Provides type check / casting functionality for schema_factory classes.
"""

__all__ = ('NodeType', 'NodeTypeError', 'Integer', 'Float', 'String', 'Boolean', 'Mapping',
           'Timestamp', 'Schema')


import ujson
from datetime import datetime
from collections import OrderedDict
from schema_factory.errors import NodeTypeError


class NodeType(object):
    """Base SchemaNode Type placeHolder.
    """

    base_type = None

    cast_callback = None

    @property
    def cast_type(self):
        """Give priority to instance type versus class base type
        """
        return self._cast_type if hasattr(self, '_cast_type') else self.base_type

    def validate(self, value):
        """Base validation method. Check if type is valid, or try brute casting.

        Args:
            value (object): A value for validation.

        Returns:
            Base_type instance.

        Raises:
            SchemaError, if validation or type casting fails.
        """

        cast_callback = self.cast_callback if self.cast_callback else self.cast_type

        try:
            return value if isinstance(value, self.cast_type) else cast_callback(value)

        except Exception:
            raise NodeTypeError('Invalid value {} for {}.'.format(value, self.cast_type))

    def __repr__(self):  # pragma: no cover
        return '<{} instance at: 0x{:x}>'.format(self.__class__, id(self))

    def __str__(self):  # pragma: no cover
        return '{}(<{}>)'.format(self.__class__.__name__, self.base_type)

    __call__ = validate


class Integer(NodeType):
    """Integer NodeType.

    >>> int_validator = Integer()
    >>> print(int_validator(34))
    34
    >>> print(int_validator('123'))
    123
    >>> print(int_validator('123c'))
    Traceback (most recent call last):
        ...
    node_types.NodeTypeError: Invalid value 123c for <class 'int'>.
    """

    __slots__ = ()

    base_type = int


class Float(NodeType):
    """Float NodeType.

    >>> float_validator = Float()
    >>> print(float_validator(34))
    34.0
    >>> print(float_validator('123.009'))
    123.009
    >>> print(float_validator('123c'))
    Traceback (most recent call last):
        ...
    node_types.NodeTypeError: Invalid value 123c for <class 'float'>.
    """

    __slots__ = ('_cast_type',)

    base_type = float


class String(NodeType):
    """String NodeType.

    >>> str_validator = String()
    >>> print(str_validator(34))
    34
    >>> print(str_validator(False))
    False
    """

    __slots__ = ()

    base_type = str


class Boolean(NodeType):
    """Boolean NodeType.

    >>> boolean_validator = Boolean()
    >>> boolean_validator(True)
    True
    >>> boolean_validator('FALSE')
    False
    >>> boolean_validator('TrUe')
    True
    """
    __slots__ = ('_cast_type',)

    base_type = bool

    cast_callback = lambda _, value: ujson.loads(value.lower())


class Timestamp(NodeType):
    """Datetime NodeType.

    >>> datetime_validator = Timestamp()
    >>> print(datetime_validator('2016-01-28 15:30:26.979879+01'))
    2016-01-28 15:30:26
    >>> print(datetime_validator('2016-01-28 15:30:26.979879'))
    2016-01-28 15:30:26
    """

    __slots__ = ('_cast_type',)

    base_type = datetime

    cast_callback = lambda _, value: datetime.strptime(value.split('.')[0], '%Y-%m-%d %H:%M:%S')


class Mapping(NodeType):
    """Mapping NodeType

    >>> mapping_validator = Mapping()
    >>> print(mapping_validator({'a': 1}))
    {'a': 1}
    >>> print(mapping_validator('{"b": 2}'))
    {'b': 2}
    """
    __slots__ = ('_cast_type',)

    base_type = (dict, OrderedDict, )

    cast_callback = lambda _, value: ujson.loads(value)


class Schema(NodeType):
    """Class instance type.

    >>> class MyClass(object):
    ...     def __init__(self, a, b):
    ...         self.a = a
    ...         self.b = b
    ...
    ...     @property
    ...     def to_dict(self):
    ...         return {'a': self.a, 'b': self.b}
    ...
    ...     def __repr__(self):
    ...         return 'MyClass({})'.format(self.a)
    ...     __str__ = __repr__
    ...
    >>> class_validator = Schema(cls_type=MyClass)
    >>> class_validator_2 = Schema(cls_type=int)
    >>> print(class_validator({'a': 1, 'b': 1}))
    {'b': 1, 'a': 1}
    >>> print(class_validator(MyClass(a=2, b=2)))
    MyClass(2)
    >>> class_validator.cast_type
    <class 'types.MyClass'>
    >>> class_validator_2.cast_type
    <class 'int'>
    >>> class BadClass(object):
    ...     def __init__(self, a):
    ...         self.a = a
    ...         raise TypeError('bar')
    ...
    >>> class_validator_3 = Schema(cls_type=BadClass)
    >>> print(class_validator_3('a'))
    Traceback (most recent call last):
        ...
    types.NodeTypeError: Invalid value a for <class 'types.BadClass'>.
    """

    __slots__ = ('_cast_type', )

    def cast_callback(self, value):
        try:
            return self.cast_type(**value).to_dict

        except Exception as cast_error:
            raise NodeTypeError('Cannot cast {} to {}: {}'.format(value, self.cast_type, cast_error.args))

    def __init__(self, cls_type=None):
        self._cast_type = cls_type
        super(Schema, self).__init__()
