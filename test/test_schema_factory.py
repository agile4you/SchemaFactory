# -*- coding: utf-8 -*-
"""Unit tests for `schema_factory` project
"""

import pytest
from schema_factory import SchemaError, SchemaType
from collections import OrderedDict


def test_schema_str(mock_schema):
    """Testing schema `__str__` method.
    """
    cls_repr = "<TestSchema instance, attributes:['name', 'number', 'scores']>"

    assert str(mock_schema()) == cls_repr


def test_schema_reflection(mock_schema):
    """Testing __isinstance__ hook.
    """

    assert isinstance(mock_schema(), SchemaType)


def test_valid_schema_pass(mock_schema):
    """Testing valid schema pass.
    """

    schema_data = OrderedDict([
        ('name', 'whatever'),
        ('number', 3),
        ('scores', [1.3, 2.3, 4.5])
    ])

    schema_model = mock_schema(**schema_data)

    assert schema_model.to_dict == schema_data


def test_schema_invalid_attribute_fail(mock_schema):
    """Testing schema validation fail for invalid schema attribute.
    """

    with pytest.raises(SchemaError):
        assert mock_schema(name='whatever', this='that')


def test_schema_invalid_attribute_value_fail(mock_schema):
    """Testing schema validation fail for invalid attribute value.
    """

    with pytest.raises(AttributeError):
        assert mock_schema(name='whatever', number='365')


def test_schema_default_pass(mock_schema):
    """Testing schema validation pass for default attribute values.
    """

    default_model = OrderedDict([('name', 'this'), ('number', 1), ('scores', [])])

    assert mock_schema().to_dict == default_model


def test_schema_attr_validator_fail(mock_schema, mock_validator):
    """Testing schema validation fail for attribute value.
    """

    mock_schema.scores.validators.append(mock_validator)

    schema_data = OrderedDict([('name', 'this'), ('number', 1), ('scores', [13.5])])

    with pytest.raises(AttributeError):
        assert mock_schema(**schema_data)


def test_schema_attr_validator_pass(mock_schema):
    """Testing schema validation pass for attribute value.
    """

    schema_data = OrderedDict([('name', 'this'), ('number', 1), ('scores', [4.5])])
    assert mock_schema(**schema_data)
