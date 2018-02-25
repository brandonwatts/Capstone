from marshmallow import Schema, fields


class GeneralAPISchema(Schema):

    State = fields.Str()
    City = fields.Str()
    Zip_Code = fields.Str()
    Address = fields.Str()
    Min_Sqft = fields.Str()
    Max_Sqft = fields.Str()
    Min_Price = fields.Str()
    Max_Price = fields.Str()
    Min_Bed = fields.Str()
    Max_Bed = fields.Str()
    Pricing_Type = fields.Str()
    Build_Year = fields.Int()
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
