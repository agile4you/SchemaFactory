# -*- coding: utf-8 -*-
"""Unit tests for `schema_factory.types` module.
"""

from datetime import datetime
import pytest
from schema_factory.types import (Integer, Float, String, Boolean, Timestamp, Mapping, Schema)
from schema_factory.errors import NodeTypeError


def test_integer_type():
    """Test types.Integer validation.
    """

    integer_validator = Integer()

    assert integer_validator(33) == integer_validator('33') == 33

    with pytest.raises(NodeTypeError):
        integer_validator('number')


def test_string_type():
    """Test types.String validation.
    """

    string_validator = String()

    assert string_validator(346565) == string_validator('346565') == '346565'


def test_float_type():
    """Test types.Float validation
    """

    float_validator = Float()

    assert all([float_validator(0.23232), float_validator(100), float_validator('inf')])

    with pytest.raises(NodeTypeError):
        float_validator('Float_number')


def test_boolean_type():
    """Test types.Boolean validation.
    """
    boolean_validation = Boolean()

    assert boolean_validation(True) == boolean_validation('TrUe') is True

    with pytest.raises(NodeTypeError):
        boolean_validation('f')


def test_timestamp_validator():
    """Test types.Timestamp validation
    """

    timestamp_validation = Timestamp()

    assert timestamp_validation('2016-01-28 15:30:26.979879+01') == datetime(2016, 1, 28, 15, 30, 26)

    with pytest.raises(NodeTypeError):
        timestamp_validation('28/7/2013')


def test_mapping_validator():
    """Test types.Mapping validation.
    """

    mapping_validator = Mapping()

    assert mapping_validator({'a': 1}) == mapping_validator('{"a": 1}') == {'a': 1}

    with pytest.raises(NodeTypeError):
        mapping_validator({1, 2, 3})


def test_schema_type(mock_schema_min):
    """Test types.Schema validation.
    """

    schema_validation = Schema(mock_schema_min)

    schema_data = {'attr': 'Foo Bar'}

    assert dict(schema_validation(schema_data)) == {'attr': 'Foo Bar'}

    with pytest.raises(NodeTypeError):
        schema_validation({'foo': 'bar'})
