from distutils.core import setup
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('schema_factory/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))


setup(
    name='SchemaFactory',
    version=version,
    packages=['schema_factory'],
    url='https://github.com/agile4you/SchemaFactory',
    license='GLPv3',
    author='Papavassiliou Vassilis',
    author_email='vpapavasil@gmail.com',
    description='Python schema toolkit',
    install_requires=['ujson']
)
