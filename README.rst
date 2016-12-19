.. image:: assets/logo.png

*python schema validation made easy...*


.. image:: https://travis-ci.org/agile4you/SchemaFactory.svg?branch=master
    :target: https://travis-ci.org/agile4you/SchemaFactory

.. image:: https://coveralls.io/repos/github/agile4you/SchemaFactory/badge.svg?branch=master
    :target: https://coveralls.io/github/agile4you/SchemaFactory?branch=master


*Example Usage*

.. code:: python

        >>> from schema_factory import BaseSchema, FloatNode, StringNode, SchemaNode
        >>>
        >>> class PointSchema(BaseSchema):
        ...     lat=FloatNode()
        ...     lng=FloatNode()
        ...
        >>> point = PointSchema(lat=34, lng=29.01)
        >>> print(point.to_dict)
        OrderedDict([('lat', 34.0), ('lng', 29.01)])
        >>>
        >>> point2 = PointSchema(lat='34', lng='0')
        >>>
        >>> print(point2.to_dict)
        OrderedDict([('lat', 34.0), ('lng', 0.0)])
        >>>
        >>> class RegionSchema(BaseSchema):
        ...     name=StringNode(),
        ...     country_code=StringNode(required=True, validators=[lambda x: len(x) == 2]),
        ...     location=SchemaNode(PointSchema, default=None),
        ...     keywords=StringNode(array=True, default=[])
        ...
        >>> region = RegionSchema(name='Athens', country_code='gr', location={'lat': 32.7647, 'lng': 27.03})
        >>> print(region)
        <RegionSchema instance, attributes:['country_code', 'keywords', 'location', 'name']>
        >>> region.keywords
        []
        >>> region2 = RegionSchema(name='Athens')
        Traceback (most recent call last):
            ...
        schema.SchemaError: Missing Required Attributes: {'country_code'}
        >>> region3 = RegionSchema(name='Athens', country_code='gr', location={'lat': 32.7647, 'lng': 27.03},
        ...     foo='bar')
        Traceback (most recent call last):
            ...
        schema.SchemaError: Invalid Attributes RegionSchema for {'foo'}.
        >>> region4 = RegionSchema(name='Athens', country_code='gr', keywords=['Acropolis', 'Mousaka', 434132])
        >>> region4.to_dict