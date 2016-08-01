# -*- coding: utf-8 -*-
"""`schema_factory.node_types` module.

Provides type check / casting functionality for schema_factory classes.
"""


import ujson


class NodeTypeError(Exception):
    """Base module exception class.
    """
    pass


class NodeType(object):
    """Base SchemaNode Type placeHolder.
    """

    base_type = None

    def __init__(self, cast_callback=None, instance_type=None):
        self.cast_callback = cast_callback
        self._instance_type = instance_type

    @property
    def class_type(self):
        """Instance type takes priority to class type
        """
        return self._instance_type or self.base_type

    @property
    def cast(self):
        """Cast a string interface into NodeType.base_type object.
        """
        if self.cast_callback:
            return self.cast_callback
        return self.class_type

    def validate(self, value):
        """Base validation method. Check if type is valid, or try brute casting.

        Args:
            value (object): A value for validation.

        Returns:
            Base_type instance.

        Raises:
            SchemaError, if validation or type casting fails.
        """

        cast_callback = self.cast

        try:
            return value if isinstance(value, self.class_type) else cast_callback(value)

        except Exception:
            raise NodeTypeError('Invalid value {} for {}.'.format(value, self.class_type))

    def __repr__(self):  # pragma: no cover
        return '<{} instance at: 0x{:x}>'.format(self.__class__, id(self))

    def __str__(self): # pragma: no cover
        return '{}(<{}>)'.format(self.__class__.__name__, self.base_type)

    __call__ = validate


class IntegerType(NodeType):
    """Integer NodeType.

    >>> int_validator = IntegerType()
    >>> print(int_validator(34))
    34
    >>> print(int_validator('123'))
    123
    >>> print(int_validator('123c'))
    Traceback (most recent call last):
        ...
    node_types.NodeTypeError: Invalid value 123c for <class 'int'>.
    """

    base_type = int


class FloatType(NodeType):
    """Float NodeType.

    >>> float_validator = FloatType()
    >>> print(float_validator(34))
    34.0
    >>> print(float_validator('123.009'))
    123.009
    >>> print(float_validator('123c'))
    Traceback (most recent call last):
        ...
    node_types.NodeTypeError: Invalid value 123c for <class 'float'>.
    """

    base_type = float


class StringType(NodeType):
    """String NodeType.

    >>> str_validator = StringType()
    >>> print(str_validator(34))
    34
    >>> print(str_validator(False))
    False
    """

    base_type = str


class BooleanType(NodeType):
    """Boolean NodeType.

    >>> boolean_validator = BooleanType()
    >>> boolean_validator(True)
    True
    >>> boolean_validator('FALSE')
    False
    >>> boolean_validator('TrUe')
    True
    """

    base_type = bool

    cast_callback = lambda _, value: ujson.loads(value.lower())
