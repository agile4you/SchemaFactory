# -*- coding: utf-8 -*-
"""`schema_factory.factory` module.

Provides schema factory utilities.
"""

__all__ = ['schema_factory', 'SchemaError', 'SchemaType']
__authors__ = 'Papavassiliou Vassilis'
__date__ = '2016-8-1'
__version__ = '1.2'


from collections import OrderedDict
from schema_factory.nodes import BaseNode


version = list(map(int, __version__.split('.')))


class SchemaError(Exception):
    """Raises when a Schema error occurs.
    """
    pass


class SchemaType(type):
    """Base Type for Schema classes.
    """

    def __new__(mcs, name, bases, attrs):

        nodes_methods = {k: v for k, v in attrs.items() if
                         isinstance(v, BaseNode)}

        for node, attr in nodes_methods.items():
            attr.alias = node

        return super(SchemaType, mcs).__new__(mcs, name, bases, attrs)


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

    return SchemaType('{}Schema'.format(schema_name.title()), (), schema_dict)
