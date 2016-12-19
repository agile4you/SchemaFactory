# -*- coding: utf-8 -*-
"""Unit tests for `schema_factory.schema` module
"""

import pytest
from schema_factory.errors import SchemaError
from collections import OrderedDict


def test_schema_required_fail(mock_schema):
    """Testing `TestSchema` `__init__` method.
    """

    with pytest.raises(SchemaError):
        mock_schema(name='Foo')


def test_schema_invalid_attr_fail(mock_schema):
    """Testing `TestSchema` `__init__` method.
    """

    with pytest.raises(SchemaError):
        mock_schema(foo='foo', name='Bar', scores=[0.34])


def test_schema_init_pass(mock_schema):
    """Testing `TestSchema` `__init__` method.
    """

    assert mock_schema(name='Bar', scores=[0.34])


def test_base_schema_subclass(mock_base_schema_subclass):
    """Testing BaseSchema subclass.
    """

    with pytest.raises(SchemaError):
        mock_base_schema_subclass(name='Foo')

    with pytest.raises(SchemaError):
        mock_base_schema_subclass(lng=23.90)

    schema = mock_base_schema_subclass(lat='34', lng=0)

    assert schema.to_dict == OrderedDict([('lat', 34.0), ('lng', 0.0)])

    assert schema.serialize('srid') == OrderedDict([('srid', 4326)])

    assert dict(schema.serialize()) == dict(OrderedDict([('lng', 0.0), ('lat', 34.0), ('srid', 4326)]))

    with pytest.raises(SchemaError):
        schema.serialize('bar')
