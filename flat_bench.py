# -*- coding: utf-8 -*-
"""Benchmarks with famous validation libraries.
"""
import cProfile
from schema_factory import BaseSchema, IntegerNode, StringNode


object_list = [{'attr_1': str(x), 'attr_2': x} for x in range(1, 10)]


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


if __name__ == '__main__':

    pr = cProfile.Profile()
    pr.enable()

    a = [TestSchema(**obj) for obj in object_list]

    pr.disable()

    pr.print_stats(sort='time')


