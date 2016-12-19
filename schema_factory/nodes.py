# -*- coding: utf-8 -*-
"""`schema_factory.nodes` module.

Provides schema Node base classes.
"""

__all__ = ['BaseNode', 'IntegerNode', 'FloatNode', 'StringNode', 'BooleanNode', 'TimestampNode', 'MappingNode',
           'SchemaNode']

__authors__ = 'Papavassiliou Vassilis'
__date__ = '2016-8-1'
__version__ = '1.6'


import weakref
from schema_factory.errors import NodeTypeError, SchemaNodeError, SchemaNodeValidatorError
from schema_factory.types import (Integer, Float, String, Boolean, Timestamp, Schema, Mapping)


class BaseNode(object):
    """Base Node descriptor class.

    Provides an attribute set/get access with type validation.

    Attributes:
        _cache (object): A key/value instance that stores per instance values.
        alias(str): The alias of the attribute at the attached class.
    """

    base_field_type = None
    base_default = None
    array = None
    base_validators = []
    base_required = None

    def __init__(self, field_type=None, alias='', array=False, validators=None, default=None, required=False):
        self._cache = weakref.WeakKeyDictionary()
        self._validators = validators or []
        self._field_type = field_type
        self._array = array
        self.alias = alias
        self._default = default
        self._required = required

    @property
    def required(self):
        return self.base_required if self.base_required is not None else self._required

    @property
    def field_type(self):
        return self.base_field_type or self._field_type

    @property
    def is_array(self):
        return self.array if self.array is not None else self._array

    @property
    def default(self):
        return self.base_default or self._default

    @property
    def validators(self):
        return (self.base_validators or []) + (self._validators or [])

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

        value = self._cache.get(instance) if self._cache.get(instance) is not None else self.default

        if hasattr(instance, 'prepare_' + self.alias):
            return getattr(instance, 'prepare_' + self.alias)(value)

        return value

    def __set__(self, instance, value):
        """Python descriptor protocol `__set__` magic method.

        Args:
            instance (object): The instance with descriptor attribute.
            value (object): The value for instance attribute.
        """

        try:
            cleaned_value = self.field_value(value)

        except NodeTypeError as node_error:
            raise SchemaNodeError('{}.{}: {}'.format(
                instance.__class__.__name__, self.alias, node_error.args[0])
            )

        try:
            self.is_valid(cleaned_value)

        except SchemaNodeValidatorError as error:
            raise SchemaNodeError(
                '{}.{} Error for {} value: {}'.format(
                    instance.__class__.__name__,
                    self.alias,
                    value,
                    error.args[0]
                )
            )

        self._cache[instance] = cleaned_value

    @staticmethod
    def validator_exc(callback):
        return callback.__msg__ if hasattr(callback, '__msg__') else callback.__doc__

    def _valid(self, value):
        if self.validators:
            for validator in self.validators:
                if not validator(value):
                    raise SchemaNodeValidatorError(self.validator_exc(validator))
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

    def __str__(self):  # pragma: no cover
        return "<{}(types: {})>".format(
            self.__class__.__name__,
            self.field_type
        )


class IntegerNode(BaseNode):
    """Concrete Integer SchemaNode.
    """
    base_field_type = Integer()


class FloatNode(BaseNode):
    """Concrete FloatNode.
    """
    base_field_type = Float()


class StringNode(BaseNode):
    """Concrete StringNode.
    """
    base_field_type = String()


class BooleanNode(BaseNode):
    """Concrete BooleanNode.
    """

    base_field_type = Boolean()


class TimestampNode(BaseNode):
    """Concrete TimestampNode.
    """

    base_field_type = Timestamp()


class MappingNode(BaseNode):
    """Concrete MappingNode.
    """
    base_field_type = Mapping()


class SchemaNode(BaseNode):
    """Concrete SchemaNode.
    """

    def __init__(self, schema, **kwargs):   # pragma: no cover
        super(SchemaNode, self).__init__(**kwargs)
        self._field_type = Schema(schema)
