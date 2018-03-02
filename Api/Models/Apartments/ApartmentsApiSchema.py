from marshmallow import Schema, fields


class ApiSchema(Schema):
    """
    This schema is used for searching https://www.apartments.com/services/search/
    """
    class Geography_Class(Schema):
        class Address_Class(Schema):
            City = fields.String()
            State = fields.String()

        GeographyType = fields.Int()
        Address = fields.Nested(Address_Class)

    class Listing_Class(Schema):
        Ratings = fields.Int()
        MinRentAmount = fields.Int()
        MaxRentAmount = fields.Int()
        MinSqft = fields.Int()
        MaxSqft = fields.Int()
        Amenities = fields.Int()

    Geography = fields.Nested(Geography_Class)
    Listing = fields.Nested(Listing_Class)
