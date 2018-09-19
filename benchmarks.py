# -*- coding: utf-8 -*-
"""Benchmarks with famous validation libraries.
"""

from schema_factory import BaseSchema, IntegerNode, StringNode
from voluptuous import Schema, Required
import colander
import serpy
import time


def timer(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te - ts))
        return result

    return timed


def object_loader():
    return [{'attr_1': str(x), 'attr_2': x} for x in range(1, 10000)]


@timer
def bench_factory():
    """Benchmark for 1000 objects with 2 fields.
    """

    class TestSchema(BaseSchema):
        attr_1 = StringNode()
        attr_2 = IntegerNode()

        @property
        def attr_3(self):
            return 'FooBar'

        @staticmethod
        def prepare_attr_1(value):
            return 'Attr#{}'.format(value)

        @staticmethod
        def prepare_attr_2(value):
            return 'Attr#2{}'.format(value)

    return [TestSchema(**obj) for obj in object_loader()]


@timer
def bench_colander():
    """
    """

    class Bench(colander.MappingSchema):
        attr_1 = colander.SchemaNode(colander.String())
        attr_2 = colander.SchemaNode(colander.Int())

    return [Bench(**obj).serialize() for obj in object_loader()]


@timer
def bench_voluptuous():
    """Benchmark for 1000 objects with 2 fields.
    """
    schema = Schema({
        Required('attr_1'): str,
        Required('attr_2'): int})

    return [schema(obj) for obj in object_loader()]


@timer
def bench_serpy():
    """Beanchmark for 1000 objects with 2 fields.
    """

    class FooSerializer(serpy.DictSerializer):
        """The serializer schema definition."""
        # Use a Field subclass like IntField if you need more validation.
        attr_2 = serpy.IntField()
        attr_1 = serpy.StrField()

    return [FooSerializer(obj).data for obj in object_loader()]


if __name__ == '__main__':

    bench_voluptuous()
    bench_factory()
    bench_colander()
    bench_serpy()

