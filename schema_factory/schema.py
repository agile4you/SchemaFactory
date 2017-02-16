# -*- coding: utf-8 -*-
"""`schema_factory.schema` module.

Provides schema factory utilities.
"""

__all__ = ['schema_factory', 'SchemaError', 'SchemaType', 'BaseSchema']
__authors__ = 'Papavassiliou Vassilis'
__date__ = '2016-8-1'
__version__ = '1.2'


from collections import OrderedDict
from schema_factory.errors import (SchemaError, SchemaNodeError)
from schema_factory.nodes import BaseNode


version = list(map(int, __version__.split('.')))


class SchemaType(type):
    """Base Type for Schema classes.
    """

    def __new__(mcs, name, bases, attrs):

        schema_nodes = {k: v for k, v in attrs.items() if
                        isinstance(v, BaseNode)}

        property_nodes = {k: v for k, v in attrs.items() if
                          isinstance(v, property) and k != 'to_dict'}

        for node, attr in schema_nodes.items():
            attr.alias = node

        attrs['schema_nodes'] = sorted(schema_nodes.keys())

        attrs['property_nodes'] = sorted(property_nodes.keys())

        attrs['data_nodes'] = set(sorted(attrs['schema_nodes'] + attrs['property_nodes']))

        attrs['required'] = {node for node in schema_nodes.keys()
                             if schema_nodes[node].required is True}

        return super(SchemaType, mcs).__new__(mcs, name, bases, attrs)


class BaseSchema(object, metaclass=SchemaType):
    """Base Schema class.

    Implements a base class for creating declarative schema.


    Examples:

        >>> from schema_factory import FloatNode
        >>> class PointSchema(BaseSchema):
        ...     lat=FloatNode()
        ...     lng=FloatNode()
        ...
        >>> point = PointSchema(lat='34.0', lng=0)
        >>> print(point.to_dict)
        OrderedDict([('lat', 34.0), ('lng', 0.0)])
    """
    def __init__(self, **kwargs):

        kwargs_set = set(kwargs)

        if not self.required.issubset(kwargs_set):
            raise SchemaError('Missing Required Attributes: {}'.format(
                self.required.difference(kwargs_set)
            ))

        if not set(kwargs).issubset(set(self.schema_nodes)):
            raise SchemaError('Invalid Attributes {} for {}.'.format(
                self.__class__.__name__,
                set(kwargs).difference(set(self.schema_nodes))
            ))

        for attr_name in kwargs:
            setattr(self, attr_name, kwargs[attr_name])

    def __repr__(self):  # pragma: no cover
        return '<{} instance at: 0x{:x}>'.format(self.__class__, id(self))

    def __str__(self):  # pragma: no cover
        return "<{} instance, attributes:{}>".format(
            self.__class__.__name__,
            self.schema_nodes
        )

    @property
    def to_dict(self):
        return OrderedDict([(k, getattr(self, k)) for k in self.schema_nodes])

    def serialize(self, *fields):
        """Serialize Nodes and attributes
        """
        if fields:
            if not set(fields).issubset(self.data_nodes):
                raise SchemaError('Invalid field for serialization: {}'.format(set(fields).difference(self.data_nodes)))

            return OrderedDict([(k, getattr(self, k)) for k in fields])

        return OrderedDict([(k, getattr(self, k)) for k in self.data_nodes])


def schema_factory(schema_name, **schema_nodes):
    """Schema Validation class factory.

    Args:
        schema_name(str): The namespace of the schema.
        schema_nodes(dict): The attr_names / SchemaNodes mapping of schema.

    Returns:
        A Schema class.

    Raises:
        SchemaError, for bad attribute setting initialization.

    Examples:

        >>> from schema_factory import FloatNode, StringNode, SchemaNode
        >>>
        >>> PointSchema = schema_factory(
        ...     schema_name='point',
        ...     lat=FloatNode(),
        ...     lng=FloatNode(),
        ... )
        ...
        >>> point = PointSchema(lat=34, lng=29.01)
        >>> print(point.to_dict)
        OrderedDict([('lat', 34.0), ('lng', 29.01)])
        >>> point2 = PointSchema(lat='34', lng='0')
        >>> print(point2.to_dict)
        OrderedDict([('lat', 34.0), ('lng', 0.0)])
        >>> RegionSchema = schema_factory(
        ...     schema_name='Region',
        ...     name=StringNode(),
        ...     country_code=StringNode( required=True, validators=[lambda x: len(x) == 2]),
        ...     location=SchemaNode(PointSchema, required=False, default=None),
        ...     keywords=StringNode(array=True, required=False, default=[])
        ... )
        ...
        >>> region = RegionSchema(name='Athens', country_code='gr', location={'lat': 32.7647, 'lng': 27.03})
        >>> print(region)
        <RegionSchema instance, attributes:['country_code', 'keywords', 'location', 'name']>
        >>> region.keywords
        []
        >>> region2 = RegionSchema(name='Athens')
        Traceback (most recent call last):
            ...
        schema_factory.errors.SchemaError: Missing Required Attributes: {'country_code'}
        >>> region3 = RegionSchema(name='Athens', country_code='gr', location={'lat': 32.7647, 'lng': 27.03},
        ...     foo='bar')
        Traceback (most recent call last):
            ...
        schema_factory.errors.SchemaError: Invalid Attributes RegionSchema for {'foo'}.
        >>> region4 = RegionSchema(name='Athens', country_code='gr', keywords=['Acropolis', 'Mousaka', 434132])
    """

    schema_dict = dict()
    schema_dict.update(schema_nodes)

    def cls_repr(self):  # pragma: no cover
        return "<{} instance at: 0x{:x}>".format(self.__class__, id(self))

    def cls_str(self):   # pragma: no cover
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
                set(kwargs).difference(set(self.schema_nodes))
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


if __name__ == '__main__':   # pragma: no cover

    import doctest
    doctest.testmod()
