from marshmallow import Schema, fields


class GeneralAPISchema(Schema):

    State = fields.Str()
    City = fields.Str()
    Zip_Code = fields.List(fields.Str())
    Address = fields.List(fields.Str())
    Min_Sqft = fields.List(fields.Str())
    Max_Sqft = fields.List(fields.Str())
    Min_Price = fields.List(fields.Str())
    Max_Price = fields.List(fields.Str())
    Min_Bed = fields.List(fields.Str())
    Max_Bed = fields.List(fields.Str())
    Pricing_Type = fields.List(fields.Str())
    Build_Year = fields.List(fields.Str())
    Dog_Friendly = fields.Bool()
    Cat_Friendly = fields.Bool()
    Has_Pool = fields.Bool()
    Has_Elevator = fields.Bool()
    Has_Fitness_Center = fields.Bool()
    Has_Wheelchair_Access = fields.Bool()
    Has_Dishwasher = fields.Bool()
    Has_Air_Conditioning = fields.Bool()
    Has_Parking = fields.Bool()
    Star_Rating = fields.List(fields.Str())
    Furnished = fields.Bool()
    Has_Laundry_Facilities = fields.Bool()
    Property_Type = fields.Str()
    Search_Radius = fields.Str()
