from marshmallow import Schema, fields


class ApartmentsSchema(Schema):
    """ This is the schema for the return value in the Apartments class."""

    class GeographyClass(Schema):
        class AddressClass(Schema):
            City = fields.String()
            State = fields.String()

        GeographyType = fields.Int()
        Address = fields.Nested(AddressClass)

    class ListingClass(Schema):
        Ratings = fields.Int()
        MinRentAmount = fields.Int()
        MaxRentAmount = fields.Int()
        MinSqft = fields.Int()
        MaxSqft = fields.Int()
        Amenities = fields.Int()

    Geography = fields.Nested(GeographyClass)
    Listing = fields.Nested(ListingClass)
