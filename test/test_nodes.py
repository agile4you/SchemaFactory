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
        number = BaseNode(field_type=Integer(), array=True, validators=[lambda x: x >= 0, lambda x: x < 50], default=40)

        @staticmethod
        def prepare_number(value):
            if not isinstance(value, (list, set, tuple)):
                return value + 10

            return [v + 10 for v in value]

    Test.number.alias = 'number'

    instance = Test()

    assert instance.number == 50

    instance.number = 10
    assert instance.number == 20

    instance.number = [30, 31]

    assert instance.number == [40, 41]

    with pytest.raises(SchemaNodeError):
        instance.number = 'String'

    with pytest.raises(SchemaNodeError):
        instance.number = -1

    with pytest.raises(SchemaNodeError):
        instance.number = 100
