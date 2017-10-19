from marshmallow import Schema, fields


__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'

class CostarApiMockSchema(Schema):
    address = fields.Str()
    country = fields.Str()
    state = fields.Str()
    city = fields.Str()
