# -*- coding: utf-8 -*-
"""`schema_factory.` module.

Provides schema factory utilities.
"""

from __future__ import absolute_import

__all__ = ['SchemaNode', 'schema_factory', 'SchemaError', 'SchemaType']
__authors__ = 'Papavassiliou Vassilis'
__date__ = '2016-1-14'
__version__ = '1.1'


from collections import OrderedDict
import ujson
from datetime import datetime
import six
import weakref


version = list(map(int, __version__.split('.')))


class SchemaError(Exception):
    """Raises when a Schema error occurs.
    """
    pass


class _SchemaType(type):
    """Base Type for Schema classes.
    """
    def __instancecheck__(self, instance):
        return 'Schema' in instance.__class__.__name__


SchemaType = _SchemaType('Schema', (), {})


class NodeType(object):
    """Base SchemaNode Type placeHolder.
    """

    base_type = None

    cast_callback = None

    @property
    def cast(self):
        """Cast a string interface into NodeType.base_type object.
        """
        if self.cast_callback:
            return self.cast_callback
        return self.base_type

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
            return value if isinstance(value, self.base_type) else cast_callback(value)

        except Exception:
            raise SchemaError('Invalid value {} for {}.'.format(value, self.base_type))

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
    schema_factory.SchemaError: Invalid value 123c for <class 'int'>.
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
    schema_factory.SchemaError: Invalid value 123c for <class 'float'>.
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


class DatetimeType(NodeType):
    """Datetime NodeType.

    >>> datetime_validator = DatetimeType()
    >>> print(datetime_validator('2016-01-28 15:30:26.979879+01'))
    2016-01-28 15:30:26
    >>> print(datetime_validator('2016-01-28 15:30:26.979879'))
    2016-01-28 15:30:26
    """

    base_type = datetime

    cast_callback = lambda _, value: datetime.strptime(value.split('.')[0], '%Y-%m-%d %H:%M:%S')


class MappingType(NodeType):
    """Mapping NodeType

    >>> mapping_validator = MappingType()
    >>> print(mapping_validator({'a': 1}))
    {'a': 1}
    >>> print(mapping_validator('{"b": 2}'))
    {'b': 2}
    """
    base_type = dict

    cast_callback = lambda _, value: ujson.loads(value)

    def __init__(self, item_type=None):
        self.item_type = item_type


class ArrayType(NodeType):
    """Array NodeType.
    """

    def __init__(self, item_type=None):
        self.base_type = item_type

    def validate(self, value):
        pass


class SchemaNode(object):
    """Base Node descriptor class.

    Provides an attribute set/get access with type validation.

    Attributes:
        _cache (object): A key/value instance that stores per instance values.
        _valid_types(tuple): A tuple of valid attribute types.
        is_array(bool): Indicates if valid types are containers.
        array_type(object): The type if array items (if is_array is True)
        alias(str): The alias of the attribute at the attached class.
    """

    _type_mapper = {
        str: six.string_types,
        int: six.integer_types,
        dict: (dict, ),
        float: (float, ),
        bool: (bool, ),
        list: (list, ),
        None: None
    }

    array_types = {list, tuple}

    def __init__(self, alias, valid_type, array_type=None, validators=None, default=None):
        self._cache = weakref.WeakKeyDictionary()
        self.validators = validators or []
        self._valid_types = self._type_mapper.get(valid_type) or (valid_type, )
        self._force_type = valid_type
        self.is_array = set(self._valid_types).issubset(self.array_types)
        self.array_type = self._type_mapper[array_type]
        self.alias = alias
        self.default = default

    def __get__(self, instance, owner):
        """Python descriptor protocol `__get__` magic method.

        Args:
            instance(object): The instance with descriptor attribute.
            owner(object): Instance class.

        Returns:
            The cached value for the class instance or None.
        """
        if not instance and owner:  # pragma: no cover
            return self

        return self._cache.get(instance) or self.default

    def __set__(self, instance, value):
        """Python descriptor protocol `__set__` magic method.

        Args:
            instance (object): The instance with descriptor attribute.
            value (object): The value for instance attribute.
        """
        if not self.is_valid(value):
            raise AttributeError(
                'Invalid value {} for {}.'.format((value, ), self)
            )

        self._cache[instance] = value

    def _valid(self, value):
        if self.validators:
            return all([v(value) for v in self.validators])
        return True

    def is_valid(self, value):
        """Validate value before actual instance setting based on type.

        Args:
            value (object): The value object for validation.

        Returns:
            True if value validation succeeds else False.
        """
        if not self.array_type:
            return isinstance(value, self._valid_types) and self._valid(value)

        return all([isinstance(item, self.array_type) and self._valid(item)
                    for item in value]) and\
            isinstance(value, self._valid_types)

    def brute_validate(self, value):
        try:
            return self._force_type(value)
        except Exception:
            raise AttributeError('Cannot cast {} to {}.'.format((value, ), self._force_type))

    def __repr__(self):  # pragma: no cover
        return "<{} instance at: 0x{:x}>".format(self.__class__, id(self))

    def __str__(self):
        return "<{}(types: {}{})>".format(
            self.__class__.__name__,
            self._valid_types,
            self.array_type or ''
        )


def schema_factory(schema_name, **schema_nodes):
    """Schema Validation class factory.

    Args:
        schema_name(str): The namespace of the schema.
        schema_nodes(dict): The attr_names / SchemaNodes mapping of schema.

    Returns:
        A Schema class.

    Raises:
        SchemaFactoryError, for bad SchemaNode instance initialization.

    Examples:
        >>> class MyType(object):
        ...     def __init__(self, *args, **kwargs):
        ...         self.data = kwargs
        ...     __repr__ = lambda self: "instance"
        ...
        >>> UserSchema = schema_factory(
        ...     schema_name='user',
        ...     id=SchemaNode('id', valid_type=int, validators=[lambda x: x > 0]),
        ...     name=SchemaNode('name', valid_type=str),
        ...     model=SchemaNode('model', valid_type=MyType)
        ... )
        ...
        >>> user = UserSchema(id=34, name='Bill', model=MyType())
        >>> isinstance(user, SchemaType)
        True
        >>> print(user.to_dict)
        OrderedDict([('id', 34), ('model', instance), ('name', 'Bill')])
        >>> bad_user_attr_1 = UserSchema(id=-1, name='Bill', model=MyType())
        Traceback (most recent call last):
            ...
        AttributeError: Invalid value (-1,) for <SchemaNode(types: (<class 'int'>,))>.
        >>> bad_user_attr_2 = UserSchema(pk=34, name='Bill', model=MyType())
        Traceback (most recent call last):
            ...
        schema_factory.SchemaError: Invalid Attributes UserSchema for {'pk'}.
        >>> bad_user_val = UserSchema(id='34', name='Bill', model=MyType())
        Traceback (most recent call last):
            ...
        AttributeError: Invalid value ('34',) for <SchemaNode(types: (<class 'int'>,))>.
        >>> print(type(user))
        <class 'schema_factory.UserSchema'>
        >>> user2 = UserSchema.brute_validate(id='43', name='Bill', model={'a': 1, 'b': 2})
        >>> print(user2.to_dict)
        OrderedDict([('id', 43), ('model', instance), ('name', 'Bill')])
    """

    schema_nodes['_schema_nodes'] = sorted(schema_nodes.keys())

    def cls_repr(self):
        return "<{} instance at: 0x{:x}>".format(self.__class__, id(self))

    def cls_str(self):
        return "<{} instance, attributes:{}>".format(
            self.__class__.__name__,
            self._schema_nodes
        )

    def brute_validate(cls, **kwargs):
        if not set(kwargs).issubset(set(cls._schema_nodes)):
            raise SchemaError('Invalid Attributes {} for {}.'.format(
                cls.__name__,
                set(kwargs).difference(set(cls._schema_nodes))
            ))

        cls_kwargs = {key: getattr(cls, key).brute_validate(value) for key, value in kwargs.items()}

        return cls(**cls_kwargs)

    def cls_init(self, **kwargs):
        if not set(kwargs).issubset(set(self._schema_nodes)):
            raise SchemaError('Invalid Attributes {} for {}.'.format(
                self.__class__.__name__,
                set(kwargs).difference(set(self._schema_nodes))
            ))

        for attr_name in kwargs:
            setattr(self, attr_name, kwargs[attr_name])

    def to_dict(self):
        return OrderedDict([(k, getattr(self, k)) for k in self._schema_nodes])

    schema_nodes['to_dict'] = property(to_dict)
    schema_nodes['__init__'] = cls_init
    schema_nodes['__repr__'] = cls_repr
    schema_nodes['__str__'] = cls_str
    schema_nodes['brute_validate'] = classmethod(brute_validate)

    return type('{}Schema'.format(schema_name.title()), (), schema_nodes)
