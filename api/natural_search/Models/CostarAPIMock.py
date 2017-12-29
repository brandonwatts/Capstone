class CostarAPIMock(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


'''
***** Unmapped Fields *****

PROPERTY USE:
pu_business_for_sale,
pu_user_properties,
pu_investment_properties,

condo_inclusion,  # Include, Only, and Exclude
portfolio_inclusion,  # Include, Only, and Exclude
country
markets
submarkets
county

# Cap Rate Range (%)
cap_rate_minimum,
cap_rate_maximum,


listing_id,
keywords,
date_entered,  # All Dates, Last 24 Hours, Last 3 Days, Last Week, 2 Weeks, Month, 3 Months, Year
property_status,
tenancy_single,  # Single or Multiple
in_unit_washer_and_dryer,
washer_and_dryer_hookups,
# Style
apartments,
houses,
condos,
townhomes,
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
