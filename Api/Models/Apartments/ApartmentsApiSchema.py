from marshmallow import Schema, fields


class ApiSchema(Schema):

    class Geography_Class(Schema):

        class Address_Class(Schema):
            City = fields.String()
            State = fields.String()

        GeographyType = fields.Int()
        Address = fields.Nested(Address_Class)

    class Listing_Class(Schema):
        Ratings = fields.Int()

    Geography = fields.Nested(Geography_Class)
    Listing = fields.Nested(Listing_Class)
