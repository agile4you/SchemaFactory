from schema_factory import (schema_factory, SchemaError, IntegerNode, FloatNode, StringNode, SchemaNode, MappingNode)
import requests


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


Image = schema_factory(
    schema_name='Image',
    uri=StringNode(),
    layer=StringNode(validators=[lambda x: x in {'overview', 'detailed'}]),
    destination_id=StringNode(),
    image_id=StringNode()
)

Tag = schema_factory(
    schema_name='Tag',
    id=IntegerNode(),
    name=StringNode(),
    score=IntegerNode(),
    tag_uri=StringNode(required=False, default='')
)

Weather = schema_factory(
    schema_name='Weather',
    humidity=StringNode(),
    sunshine=StringNode(),
    wind_speed=StringNode(),
    temperature=StringNode(),
    airport_ref=StringNode()
)

Places = schema_factory(
    schema_name='Places',
    beach=IntegerNode(required=False, default=0),
    port=IntegerNode(required=False, default=0),
    hotel=IntegerNode(required=False, default=0),
    marina=IntegerNode(required=False, default=0),
    residential=IntegerNode(required=False, default=0),
    anchorage=IntegerNode(required=False, default=0)
)

Destination = schema_factory(
    schema_name='Destination',
    id=StringNode(),
    type=StringNode(),
    name=StringNode(),
    slug=StringNode(),
    breadcrumb=StringNode(array=True),
    country_code=StringNode(),
    description=StringNode(),
    description_url=StringNode(required=False, default='www.tripinview.com'),
    destination_rel=StringNode(array=True, required=False, default=[]),
    point=SchemaNode(Point),
    bound=SchemaNode(Bound),
    images=SchemaNode(Image, array=True),
    tags=SchemaNode(Tag, array=True),
    weather=SchemaNode(Weather),
    image_count=IntegerNode(),
    video_count=IntegerNode(),
    places=SchemaNode(Places),
    user_data=MappingNode(required=False, default={})
)


#  Validate remote object.


destination_data = requests.get('https://api02.tripinview.com/resources/destination/50015').json().get('data')

destination = Destination(**destination_data)


print(destination.tags)

