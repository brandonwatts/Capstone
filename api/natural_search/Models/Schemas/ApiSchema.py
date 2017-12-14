from marshmallow import Schema, fields

"""APISchema.py is the Schema for the APIResponse.py object"""

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'


class ApiSchema(Schema):
    state = fields.List(fields.Str())
    city = fields.List(fields.Str())
    zip_code = fields.List(fields.Str())
    min_sqft = fields.List(fields.Str())
    max_sqft = fields.List(fields.Str())
    min_price = fields.List(fields.Str())
    max_price = fields.List(fields.Str())
    min_bed = fields.List(fields.Str())
    max_bed = fields.List(fields.Str())
    pricing_type = fields.List(fields.Str())
    address = fields.List(fields.Str())
    build_year = fields.List(fields.Str())
    dog_friendly = fields.Bool()
    cat_friendly = fields.Bool()
    has_pool = fields.Bool()
    has_elevator = fields.Bool()
    has_fitness_center = fields.Bool()
    has_wheelchair_access = fields.Bool()
    has_dishwasher = fields.Bool()
    has_air_conditioning = fields.Bool()
    has_parking = fields.Bool()
    star_rating = fields.Int()
    is_furnished = fields.Bool()
    has_laundry_facilities = fields.Bool()
