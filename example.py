from schema_factory import (schema_factory, SchemaNode, Float, Integer, Schema, String, SchemaError)
import re


def email_validator(email):
    """Invalid email.
    """
    return re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email)


Point = schema_factory(
    schema_name='Point',
    lat=SchemaNode('lat', Float()),
    lng=SchemaNode('lng', Float())
)

Bound = schema_factory(
    schema_name='Bound',
    southwest=SchemaNode('southwest', Schema(Point)),
    northeast=SchemaNode('northeast', Schema(Point))
)


Entity = schema_factory(
    schema_name='Entity',
    id=SchemaNode('id', Integer()),
    name=SchemaNode('name', String()),
    email=SchemaNode('name', String(), validators=[email_validator]),
    bound=SchemaNode('bound', Schema(Bound)),
    points=SchemaNode('points', Schema(Point), array=True, required=False, default=[])
)


class PositiveInteger(SchemaNode):
    field_type = Int
    validators = [lambda x: x >= 0]


entity = Entity(
    id='1232323',
    name='Greece, Cyclades, Mykonos',
    bound={
        "northeast": {"lat": 40.232917785645, "lng": 26.817279815674},
         "southwest": {"lat": 39.915752410889, "lng": 26.159860610962}
    },
    points=[{'lat': 1, 'lng': 0.08}, {'lat': '34.9898', 'lng': '0.9788347'}],
    email='pav@gmail.com'
)


print(entity.to_dict)

