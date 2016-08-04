# -*- coding: utf-8 -*-
"""`schema_factory.schema_factory` module.

Provides schema factory utilities.
"""

__all__ = ['SchemaNode', 'schema_factory', 'SchemaError', 'SchemaType']
__authors__ = 'Papavassiliou Vassilis'
__date__ = '2016-8-1'
__version__ = '1.2'


from collections import OrderedDict
import ujson
import weakref
from schema_factory.node_types import NodeTypeError


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

    def __init__(self, alias, field_type, array=False, validators=None, default=None, required=True):
        self._cache = weakref.WeakKeyDictionary()
        self.validators = validators or []
        self.field_type = field_type
        self.is_array = array
        self.alias = alias
        self.default = default
        self.required = required

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

        try:
            cleaned_value = self.field_value(value)

        except NodeTypeError as node_error:
            raise AttributeError(node_error.args[0])

        if not self.is_valid(cleaned_value):
            raise AttributeError(
                'Invalid value {} for {}.'.format((value,), self)
            )

        self._cache[instance] = cleaned_value

    @staticmethod
    def validator_exc(callback):
        return callback.__doc__ if hasattr(callback, '__doc__') else callback.__name__

    def _valid(self, value):
        if self.validators:
            for validator in self.validators:
                if not validator(value):
                    raise SchemaError('Invalid value {}: {}'.format(value, self.validator_exc(validator)))
            # return all([v(value) for v in self.validators])
            return True
        return True

    def field_value(self, value):
        """Validate against NodeType.
        """
        if not self.is_array:
            return self.field_type(value)
        return [self.field_type(item) for item in value]

    def is_valid(self, value):
        """Validate value before actual instance setting based on type.

        Args:
            value (object): The value object for validation.

        Returns:
            True if value validation succeeds else False.
        """
        if not self.is_array:
            return self._valid(value)

        return all([self._valid(item) for item in value])

    def __repr__(self):  # pragma: no cover
        return "<{} instance at: 0x{:x}>".format(self.__class__, id(self))

    def __str__(self):
        return "<{}(types: {})>".format(
            self.__class__.__name__,
            self.field_type
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
        >>>
        >>> class MyType(object):
        ...     def __init__(self, **kwargs):
        ...         self.data = kwargs
        ...     __repr__ = lambda self: "instance"
        ...
        >>> UserSchema = schema_factory(
        ...     schema_name='user',
        ...     id=SchemaNode('id', fields.Integer(), validators=[lambda x: x >=1], required=False),
        ...     name=SchemaNode('id', fields.String(), validators=[lambda x: len(x) <= 10 ]),
        ...     model=SchemaNode('model', fields.Instance(MyType))
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
        AttributeError: Invalid value (-1,) for <SchemaNode(types: IntegerType(<<class 'int'>>))>.
        >>> bad_user_attr_2 = UserSchema(pk=34, name='Bill', model=MyType())
        Traceback (most recent call last):
            ...
        schema_factory.SchemaError: Invalid Attributes UserSchema for {'pk'}.
        >>> cast_user_val = UserSchema(id='34', name='Bill', model={'a': 1})
        >>> print(cast_user_val.to_dict)
        OrderedDict([('id', 34), ('model', instance), ('name', 'Bill')])
        >>> print(type(user))
        <class 'schema_factory.UserSchema'>
        >>> partial_user = UserSchema(name='Alison', model={'b': 1})
        >>> print(partial_user.to_dict)
        OrderedDict([('id', None), ('model', instance), ('name', 'Alison')])
    """

    schema_dict = dict()
    schema_dict.update(schema_nodes)

    schema_dict['schema_nodes'] = sorted(schema_nodes.keys())

    schema_dict['required'] = {node for node in schema_nodes.keys()
                               if schema_nodes[node].required is True}

    def cls_repr(self):
        return "<{} instance at: 0x{:x}>".format(self.__class__, id(self))

    def cls_str(self):
        return "<{} instance, attributes:{}>".format(
            self.__class__.__name__,
            self.schema_nodes
        )

    def cls_init(self, **kwargs):

        kwargs_set = set(kwargs)

        if not self.required.issubset(kwargs_set):
            raise SchemaError('Missing Required Attributes: {}'.format(
                self.required.difference(kwargs_set)
            ))

        if not set(kwargs).issubset(set(self.schema_nodes)):
            raise SchemaError('Invalid Attributes {} for {}.'.format(
                self.__class__.__name__,
                set(kwargs).difference(set(self.required))
            ))

        for attr_name in kwargs:
            setattr(self, attr_name, kwargs[attr_name])

    def to_dict(self):
        return OrderedDict([(k, getattr(self, k)) for k in self.schema_nodes])

    schema_dict['to_dict'] = property(to_dict)
    schema_dict['__init__'] = cls_init
    schema_dict['__repr__'] = cls_repr
    schema_dict['__str__'] = cls_str

    return type('{}Schema'.format(schema_name.title()), (), schema_dict)
