# -*- coding: utf-8 -*-
"""`schema_factory.errors` module.

Provides package error hierarchy classes.
"""


class SchemaFactoryError(Exception):
    """Base Package Error.
    """
    pass


class NodeTypeError(SchemaFactoryError):
    """`schema_factory.types` base exception class.
    """
    pass


class SchemaNodeError(SchemaFactoryError):
    """`schema_factory.nodes` module base exception class.
    """
    pass


class SchemaNodeValidatorError(SchemaNodeError):
    """`schema_factory.nodes` module custom validator error class.
    """
    pass


class SchemaError(SchemaFactoryError):
    """`schema_factory.schema` module error class
    """
    pass
