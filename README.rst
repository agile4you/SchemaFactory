**SchemaFactory**:  *python schema made easy...*


.. image:: https://travis-ci.org/agile4you/SchemaFactory.svg?branch=master
    :target: https://travis-ci.org/agile4you/SchemaFactory

.. image:: https://coveralls.io/repos/github/agile4you/SchemaFactory/badge.svg?branch=master
    :target: https://coveralls.io/github/agile4you/SchemaFactory?branch=master


*Example Usage*

.. code:: python

        >>> class MyType(object):
        ...     __repr__ = lambda self: "instance"
        ...
        >>> UserSchema = schema_factory(
        ...     schema_name='user',
        ...     id=SchemaNode('id', valid_type=int, validators=[lambda x: x > 0]),
        ...     name=SchemaNode('name', valid_type=str),
        ...     model=SchemaNode('model', valid_type=MyType)
        ... )
        ...
        >>> user = UserSchema(id=34, name='Bill', model=MyType())
        >>> print(user.to_dict)
        OrderedDict([('id', 34), ('model', instance), ('name', 'Bill')])
        >>> bad_user_attr_1 = UserSchema(id=-1, name='Bill', model=MyType())
        Traceback (most recent call last):
            ...
        AttributeError: Invalid value (-1,) for <SchemaNode(types: (<class 'int'>,))>.
        >>> bad_user_attr_2 = UserSchema(pk=34, name='Bill', model=MyType())
        Traceback (most recent call last):
            ...
        node.SchemaError: Invalid Attributes UserSchema for {'pk'}.
        >>> bad_user_val = UserSchema(id='34', name='Bill', model=MyType())
        Traceback (most recent call last):
            ...
        AttributeError: Invalid value ('34',) for <SchemaNode(types: (<class 'int'>,))>.