from schema_factory import (schema_factory, SchemaError, IntegerNode, FloatNode, StringNode, SchemaNode,)
import re
from functools import wraps


def validator(msg=''):
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


@validator('Malformed Email format.')
def email_validator(email):
    """Invalid email.
    """
    return re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email)


Point = schema_factory(
    schema_name='Point',
    lat=FloatNode(),
    lng=FloatNode()
)


Bound = schema_factory(
    schema_name='Bound',
    southwest=SchemaNode(Point),
    northeast=SchemaNode(Point)
)


@validator('Age must be between 18 and 30.')
def age_validator(age):
    """Age validator
    """
    return 18 <= age <= 30

Entity = schema_factory(
    schema_name='Entity',
    id=IntegerNode(),
    age=IntegerNode(validators=[age_validator]),
    name=StringNode(),
    email=StringNode(validators=[email_validator]),
    bound=SchemaNode(Bound),
    points=SchemaNode(Point, array=True, required=False, default=[])
)

entity = Entity(
    id='1232323',
    age='33',
    name='Greece, Cyclades, Mykonos',
    bound={
        "northeast": {"lat": 40.232917785645, "lng": 26.817279815674},
         "southwest": {"lat": 39.915752410889, "lng": 26.159860610962}
    },
    points=[{'lat': '1', 'lng': 0.08}, {'lat': '34.9898', 'lng': '0.9788347'}],
    email='pav@gmail.com'
)


print(entity.to_dict)

