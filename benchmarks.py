# -*- coding: utf-8 -*-
"""Benchmarks with famous validation libraries.
"""

from schema_factory import schema_factory, IntegerNode, StringNode
from voluptuous import Schema, Required
import colander
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
    return [{'attr_1': str(x), 'attr_2': x} for x in range(1, 100000)]


@timer
def bench_factory():
    """Benchmark for 1000 objects with 2 fields.
    """

    schema_f = schema_factory(
        schema_name='bench',
        attr_1=StringNode(),
        attr_2=IntegerNode()
    )

    return [schema_f(**obj) for obj in object_loader()]


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

if __name__ == '__main__':

    bench_voluptuous()
    bench_factory()
    bench_colander()
