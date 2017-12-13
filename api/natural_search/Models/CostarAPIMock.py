__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'


class CostarAPIMock(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


'''
***** Unmapped Fields *****

PROPERTY TYPE:
pt_industrial
pt_retail
pt_shopping_center
pt_multifamily
pt_specialty
pt_office
pt_health_care
pt_hospitality
pt_sports_and_entertainment
pt_land
pt_residential_income

PROPERTY USE:
pu_business_for_sale,
pu_user_properties,
pu_investment_properties,

# Condos
condo_inclusion,  # Include, Only, and Exclude
# Portfolios
portfolio_inclusion,  # Include, Only, and Exclude
# Country
country,
# Market
markets,
# SubMarket
submarkets,
# County
county,

# Search within x miles
search_radius

# Lot Size Range
lot_size_minimum,
lot_size_maximum,
lot_size_metric,  # Acres, Square Foot, Hectares, Square Meters

# Units/Rooms/Beds Range
bed_range_minimum,
bed_range_maximum,

# Cap Rate Range (%)
cap_rate_minimum,
cap_rate_maximum,

# Year Built
year_built_minimum,
year_built_maximum,

listing_id,
keywords,
date_entered,  # All Dates, Last 24 Hours, Last 3 Days, Last Week, 2 Weeks, Month, 3 Months, Year
property_status,
tenancy_single,  # Single or Multiple
air_conditioning,
in_unit_washer_and_dryer,
washer_and_dryer_hookups,
dishwasher,
wheelchair_access,
parking,
laundry_facilities,
fitness_center,
pool,
elevator,
dog_friendly,
cat_friendly,
furnished,
# Style
apartments,
houses,
condos,
townhomes,
# Rating
five_star,
four_star,
three_star,
two_star,
# Specialties
senior_housing,
military_housing,
student_housing,
corporate_housing,
affordable,
luxury,
cheap,
short_term,
'''
