# -*- coding: utf-8 -*-
"""`schema_factory.` module.

Provides schema factory utilities.
"""

from __future__ import absolute_import

__all__ = ['SchemaNode', 'schema_factory', 'SchemaError', 'Schema']
__authors__ = 'Papavassiliou Vassilis'
__date__ = '2016-1-14'


from schema_factory import __version__
from collections import OrderedDict
import six
import weakref


version = list(map(int, __version__.split('.')))


class SchemaError(Exception):
    """Raises when a Schema error occurs.
    """
    pass


class SchemaType(type):
    """Base Type for Schema classes.
    """
    def __instancecheck__(self, instance):
        return 'Schema' in instance.__class__.__name__


Schema = SchemaType('Schema', (), {})


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

    def __init__(self, alias, valid_type, array_type=None, validators=None,
                 default=None):
        self._cache = weakref.WeakKeyDictionary()
        self.validators = validators or []
        self._valid_types = self._type_mapper.get(valid_type) or (valid_type, )
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
        >>> isinstance(user, Schema)
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
        __init__.SchemaError: Invalid Attributes UserSchema for {'pk'}.
        >>> bad_user_val = UserSchema(id='34', name='Bill', model=MyType())
        Traceback (most recent call last):
            ...
        AttributeError: Invalid value ('34',) for <SchemaNode(types: (<class 'int'>,))>.
    """

    schema_nodes['_schema_nodes'] = sorted(schema_nodes.keys())

    def cls_repr(self):
        return "<{} instance at: 0x{:x}>".format(self.__class__, id(self))

    def cls_str(self):
        return "<{} instance, attributes:{}>".format(
            self.__class__.__name__,
            self._schema_nodes
        )

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

    return type('{}Schema'.format(schema_name.title()), (), schema_nodes)
