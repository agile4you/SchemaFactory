.. image:: assets/logo.png

*python schema validation made easy...*


.. image:: https://travis-ci.org/agile4you/SchemaFactory.svg?branch=master
    :target: https://travis-ci.org/agile4you/SchemaFactory

.. image:: https://coveralls.io/repos/github/agile4you/SchemaFactory/badge.svg?branch=master
    :target: https://coveralls.io/github/agile4you/SchemaFactory?branch=master


*Example Usage*

.. code:: python

        >>> PointSchema = schema_factory(
        ...     schema_name='point',
        ...     lat=FloatNode(),
        ...     lng=FloatNode(),
        ... )
        ...
        >>> point = PointSchema(lat=34, lng=29.01)
        >>> print(point.to_dict)
        OrderedDict([('lat', 34.0), ('lng', 29.01)])