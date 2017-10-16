from marshmallow import Schema, fields

"""APISchema.py is the Schema for the APIResponse.py object"""

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'

class ApiSchema(Schema):
    tokens = fields.List(fields.Str())
    POSTags = fields.List(fields.List(fields.Str()))
