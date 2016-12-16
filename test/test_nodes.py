# -*- coding: utf-8 -*-
"""Unit tests for `schema_factory.nodes` module.
"""


import pytest
from schema_factory.nodes import BaseNode, Integer
from schema_factory.errors import SchemaNodeError


def test_base_node_node_validation():
    """Test nodes.IntegerNode.
    """

    class Test(object):
        number = BaseNode(field_type=Integer(), validators=[lambda x: x >= 0, lambda x: x < 50], default=40)

        @staticmethod
        def prepare_number(value):
            return value + 10

    Test.number.alias = 'number'

    instance = Test()

    assert instance.number == 50

    instance.number = 10
    assert instance.number == 20

    with pytest.raises(SchemaNodeError):
        instance.number = 'String'

    with pytest.raises(SchemaNodeError):
        instance.number = -1

    with pytest.raises(SchemaNodeError):
        instance.number = 100
