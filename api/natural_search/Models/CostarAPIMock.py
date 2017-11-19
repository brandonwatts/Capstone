__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'


class CostarAPIMock(object):
    def __init__(self,
                 pt_industrial,
                 pt_retail,
                 pt_shopping_center,
                 pt_multifamily,
                 pt_specialty,
                 pt_office,
                 pt_health_care,
                 pt_hospitality,
                 pt_sports_and_entertainment,
                 pt_land,
                 pt_residential_income,
                 # Property Use:
                 pu_business_for_sale,
                 pu_user_properties,
                 pu_investment_properties,
                 # Condos
                 condo_inclusion,  # Include, Only, and Exclude
                 # Portfolios
                 portfolio_inclusion,  # Include, Only, and Exclude

                 # --- Section 2: Location ---
                 # Country
                 country,
                 # States
                 states,
                 # Market
                 markets,
                 # SubMarket
                 submarkets,
                 # County
                 county,
                 # City
                 city,
                 # ZIP Code
                 zip_code,
                 # Street Address or Intersection
                 street_address,
                 # Search within x miles
                 search_radius,

                 # --- Section 3: Criteria ---
                 # Prince Range ($)
                 price_minimum,
                 price_maximum,
                 pricing_type,  # Total $, $ Per Square Foot, $ Per Acre, or $ Per Unit
                 # Total Building Size Per Square Foot
                 building_size_minimum,
                 building_size_maximum,
                 building_size_metric,  # Square Foot or Square Meter
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

                 # --- Section 4: Other ---
                 # Listing ID
                 listing_id,
                 # Keyword
                 keywords,
                 # Date Entered
                 date_entered,  # All Dates, Last 24 Hours, Last 3 Days, Last Week, 2 Weeks, Month, 3 Months, Year
                 # Property Status
                 property_status,
                 # Only Net-Leased Properties, Include Pending Sales, Only Distressed Properties, Only Property Auctions
                 # Tenancy
                 tenancy_single,  # Single or Multiple



                 # ---------- Gathered From Apartments.com Filters ----------
                 # Interior & Community Amenities
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
                 # Square Feet
                 square_feet_minimum,
                 # No Min, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2500, 3000, 3500, 4000, 4500
                 square_feet_maxiumum):  # Same as above

        self.pt_industrial = pt_industrial
        self.pt_retail = pt_retail
        self.pt_shopping_center = pt_shopping_center
        self.pt_multifamily = pt_multifamily
        self.pt_specialty = pt_specialty
        self.pt_office = pt_office
        self.pt_health_care = pt_health_care
        self.pt_hospitality = pt_hospitality
        self.pt_sports_and_entertainment = pt_sports_and_entertainment
        self.pt_land = pt_land
        self.pt_residential_income = pt_residential_income

        self.pu_business_for_sale = pu_business_for_sale
        self.pu_user_properties = pu_user_properties
        self.pu_investment_properties = pu_investment_properties
        self.condo_inclusion = condo_inclusion
        self.portfolio_inclusion = portfolio_inclusion

        self.country = country
        self.states = states
        self.markets = markets
        self.submarkets = submarkets
        self.county = county
        self.city = city
        self.zip_code = zip_code
        self.street_address = street_address
        self.search_radius = search_radius

        self.price_minimum = price_minimum
        self.price_maximum = price_maximum
        self.pricing_type = pricing_type
        self.building_size_minimum = building_size_minimum
        self.building_size_maximum = building_size_maximum
        self.building_size_metric = building_size_metric
        self.lot_size_minimum = lot_size_minimum
        self.lot_size_maximum = lot_size_maximum
        self.lot_size_metric = lot_size_metric
        self.bed_range_minimum = bed_range_minimum
        self.bed_range_maximum = bed_range_maximum
        self.cap_rate_minimum = cap_rate_minimum
        self.cap_rate_maximum = cap_rate_maximum
        self.year_built_minimum = year_built_minimum
        self.year_built_maximum = year_built_maximum

        self.listing_id = listing_id
        self.keywords = keywords
        self.date_entered = date_entered
        self.property_status = property_status
        self.tenancy = tenancy

        self.air_conditioning = air_conditioning
        self.in_unit_washer_and_dryer = in_unit_washer_and_dryer
        self.washer_and_dryer_hookups = washer_and_dryer_hookups
        self.dishwasher = dishwasher
        self.wheelchair_access = wheelchair_access
        self.parking = parking
        self.laundry_facilities = laundry_facilities
        self.fitness_center = fitness_center
        self.pool = pool
        self.elevator = elevator
        self.dog_friendly = dog_friendly
        self.cat_friendly = cat_friendly
        self.furnished = furnished
        self.apartments = apartments
        self.houses = houses
        self.condos = condos
        self.townhomes = townhomes
        self.five_star = five_star
        self.four_star = four_star
        self.three_star = three_star
        self.two_star = two_star
        self.senior_housing = senior_housing
        self.military_housing = military_housing
        self.student_housing = student_housing
        self.corporate_housing = corporate_housing
        self.affordable = affordable
        self.luxury = luxury
        self.cheap = cheap
        self.short_term = short_term
        self.square_feet_minimum = square_feet_minimum
        self.square_feet_maxiumum = square_feet_maxiumum
