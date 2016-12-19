# -*- coding: utf-8 -*-
"""Unit test fixtures for `schema_factory` project
"""


import pytest
from schema_factory import (schema_factory, BaseSchema, IntegerNode, StringNode, FloatNode)


@pytest.fixture(scope='session')
def mock_schema_min():
    """Minimum Schema fixture.
    """

    test_schema = schema_factory(
        schema_name='MinTest',
        attr=StringNode()
    )

    return test_schema


@pytest.fixture(scope='session')
def mock_schema():
    """Schema fixture.
    """
    test_schema = schema_factory(
        schema_name='test',
        number=IntegerNode(default=0),
        name=StringNode(required=True),
        scores=FloatNode(required=True, array=True)
    )

    return test_schema


@pytest.fixture(scope='session')
def mock_base_schema_subclass():
    """BaseSchema subclass fixture.
    """

    class PointSchema(BaseSchema):
        lat = FloatNode(required=True)
        lng = FloatNode()

        @property
        def srid(self):
            return 4326

    return PointSchema


@pytest.fixture(scope='session')
def mock_validator():
    """Schema validator fixture.
    """
    return lambda x: 0.0 <= x <= 5.0
