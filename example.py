from schema_factory import BaseSchema, FloatNode, StringNode


class GeographyMixin(object):

    @property
    def srid(self):
        return 4326


class Location(GeographyMixin, BaseSchema):
    """Mock Schema example.
    """
    lat = FloatNode()
    lng = FloatNode()
    toponym = StringNode(default='')

    @staticmethod
    def prepare_toponym(value):
        if value:
            return [v.strip() for v in value.split(',')]
        return value


a = Location(lat=38.923, lng='23.98934', toponym='Greece, Athens, Ilion')


def gradient(offset: int) -> int:
    return offset - 10

gradient(int)
