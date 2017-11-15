from marshmallow import Schema, fields

"""APISchema.py is the Schema for the APIResponse.py object"""

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'


class ApiSchema(Schema):
    states = fields.List(fields.Str())
    city = fields.List(fields.Str())
    zip_code = fields.List(fields.Str())
    sq_ft = fields.List(fields.Str())
    price = fields.List(fields.Str())
