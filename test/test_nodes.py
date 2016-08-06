# -*- coding: utf-8 -*-
"""Unit tests for `schema_factory.nodes` module.
"""


import pytest
from schema_factory.nodes import BaseNode, Integer


def test_base_node_node_validation():
    """Test nodes.IntegerNode.
    """

    class Test(object):
        number = BaseNode(field_type=Integer(), validators=[lambda x: x >= 0, lambda x: x < 50], default=40)

    instance = Test()

    assert instance.number == 40

    instance.number = 10
    assert instance.number == 10

    with pytest.raises(AttributeError):
        instance.number = 'String'

    with pytest.raises(AttributeError):
        instance.number = -1

    with pytest.raises(AttributeError):
        instance.number = 100
