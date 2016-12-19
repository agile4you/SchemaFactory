.. image:: assets/logo.png

*python schema validation made easy...*


.. image:: https://travis-ci.org/agile4you/SchemaFactory.svg?branch=master
    :target: https://travis-ci.org/agile4you/SchemaFactory

.. image:: https://coveralls.io/repos/github/agile4you/SchemaFactory/badge.svg?branch=master
    :target: https://coveralls.io/github/agile4you/SchemaFactory?branch=master


*Example Usage*

.. code:: python

        >>> from schema_factory import BaseSchema, FloatNode, StringNode, SchemaNode, IntegerNode
        >>>
        >>> class PointSchema(BaseSchema):
        ...     lat=FloatNode()
        ...     lng=FloatNode()
        ...
        >>> class RegionSchema(BaseSchema):
        ...     name=StringNode()
        ...     population=IntegerNode(default=50)
        ...     country_code=StringNode(required=True, validators=[lambda x: len(x) == 2])
        ...     location=SchemaNode(PointSchema, default=None)
        ...     keywords=StringNode(array=True, default=[])
        ...
        >>> region = RegionSchema(
        ...     name='Athens',
        ...     population='1234',
        ...     country_code='gr',
        ...     location={'lat': 32.7647, 'lng': 27.03}
        ... )
        >>> print(region)
        <RegionSchema instance, attributes:['country_code', 'keywords', 'location', 'name', 'population']>
        >>> region_2 = RegionSchema(name='Athens')
        Traceback (most recent call last):
            ...
        schema.SchemaError: Missing Required Attributes: {'country_code'}
        >>> region_3 = RegionSchema(
        ...     name='Athens',
        ...     country_code='gr',
        ...     location={'lat': 32.7647, 'lng': 27.03},
        ...     foo='bar'
        ... )
        ...
        Traceback (most recent call last):
            ...
        schema.SchemaError: Invalid Attributes RegionSchema for {'foo'}.