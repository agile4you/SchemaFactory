# -*- coding: utf-8 -*-
"""Unit test fixtures for `schema_factory` project
"""


import pytest
from schema_factory import (SchemaNode, schema_factory)


@pytest.fixture(scope='session')
def mock_schema():
    """Schema fixture.
    """
    test_schema = schema_factory(
        schema_name='test',
        number=SchemaNode('number', valid_type=int, default=1),
        name=SchemaNode('name', valid_type=str, default='this'),
        scores=SchemaNode('scores', valid_type=list, array_type=float, default=[])
    )

    return test_schema


@pytest.fixture(scope='session')
def mock_validator():
    """Schema validator fixture.
    """
    return lambda x: 0.0 <= x <= 5.0
