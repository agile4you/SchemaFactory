# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015  Papavassiliou Vassilis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""`schema_factory.` module.

Provides schema factory utilities.
"""


__all__ = ['schema_factory', 'SchemaType', 'BaseNode', 'IntegerNode', 'FloatNode', 'StringNode',
           'BooleanNode', 'TimestampNode', 'MappingNode', 'SchemaNode', 'validator_message', 'BaseSchema',
           'SchemaError', 'NodeTypeError', 'SchemaNodeError', 'SchemaNodeValidatorError', 'SchemaFactoryError']

__authors__ = 'Papavassiliou Vassilis'
__date__ = '2016-8-6'
__version__ = '1.7.4'

from schema_factory.schema import *
from schema_factory.nodes import *
from schema_factory.errors import *


def validator_message(msg=''):  # pragma: no cover
    """Wraps a validator function for handling errors.
    Args:
        msg (str): The validator message.

    Returns:
        Function.
    """

    def _wrapped(func):
        func.__msg__ = msg
        return func

    return _wrapped
