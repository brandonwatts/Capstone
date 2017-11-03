from marshmallow import Schema, fields


__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'

class CostarApiMockSchema(Schema):
	# ---------- Gathered From Loopnet For Sale Filter Tab ----------
	# --- Section 1: Search Type ---
	# Property Types:
	pt_select_all = fields.Bool()
	pt_industrial = fields.Bool()
	pt_retail = fields.Bool()
	pt_shopping_center = fields.Bool()
	pt_multifamily = fields.Bool()
	pt_specialty = fields.Bool()
	pt_office = fields.Bool()
	pt_health_care = fields.Bool()
	pt_hospitality = fields.Bool()
	pt_sports_and_entertainment = fields.Bool()
	pt_land = fields.Bool()
	pt_residential_income = fields.Bool()
	# Property Use:
	pu_business_for_sale  = fields.Bool()
	pu_user_properties  = fields.Bool()
	pu_investment_properties = fields.Bool()
	# Condos
	condo_inclusion = fields.Str() # Include, Only, and Exclude
	# Portfolios
	portfolio_inclusion = fields.Str() # Include, Only, and Exclude
	
	# --- Section 2: Location ---
	# Country
	country = fields.Str()
	# States
	states = fields.Str()
	# Market
	markets = fields.Str()
	# SubMarket
	submarkets = fields.Str()
	# County
	county = fields.Str()
	# City
	city = fields.Str()
	# ZIP Code
	zip_code = fields.Str()
	# Street Address or Intersection
	street_address = fields.Str()
	# Search within x miles
	search_radius = fields.Int()
	
	# --- Section 3: Criteria ---
	# Prince Range ($)
	price_minimum = fields.Decimal()
	price_maximum = fields.Decimal()
	pricing_type = fields.Str() # Total $, $ Per Square Foot, $ Per Acre, or $ Per Unit
	# Total Building Size Per Square Foot
	building_size_minimum = fields.Decimal()
	building_size_maximum = fields.Decimal()
	building_size_metric = fields.Str() # Square Foot or Square Meter
	# Lot Size Range
	lot_size_minimum = fields.Decimal()
	lot_size_maximum = fields.Decimal()
	lot_size_metric = fields.Str() # Acres, Square Foot, Hectares, Square Meters
	# Units/Rooms/Beds Range
	bed_range_minimum = fields.Int()
	bed_range_maximum = fields.Int()
	# Cap Rate Range (%)
	cap_rate_minimum = fields.Decimal()
	cap_rate_maximum = fields.Decimal()
	# Year Built
	year_built_minimum = fields.Int()
	year_built_maximum = fields.Int()
	
	# --- Section 4: Other --- 
	# Listing ID
	listing_id = fields.Str()
	# Keyword
	keywords = fields.Str()
	# Date Entered
	date_entered = fields.Str() # All Dates, Last 24 Hours, Last 3 Days, Last Week, 2 Weeks, Month, 3 Months, Year
	# Property Status
	property_status = fields.Str() # Only Net-Leased Properties, Include Pending Sales, Only Distressed Properties, Only Property Auctions
	#Tenancy
	tenancy_single = fields.Bool() # Single or Multiple
		

		
	# ---------- Gathered From Apartments.com Filters ----------
	# Interior & Community Amenities
	air_conditioning = fields.Bool()
	in_unit_washer_and_dryer = fields.Bool()
	washer_and_dryer_hookups = fields.Bool()
	dishwasher = fields.Bool()
	wheelchair_access = fields.Bool()
	parking = fields.Bool()
	laundry_facilities = fields.Bool()
	fitness_center = fields.Bool()
	pool = fields.Bool()
	elevator = fields.Bool()
	dog_friendly = fields.Bool()
	cat_friendly = fields.Bool()
	furnished = fields.Bool()
	# Style
	apartments = fields.Bool()
	houses = fields.Bool()
	condos = fields.Bool()
	townhomes = fields.Bool()
	# Rating
	five_star = fields.Bool()
	four_star = fields.Bool()
	three_star = fields.Bool()
	two_star = fields.Bool()
	# Specialties
	senior_housing = fields.Bool()
	military_housing = fields.Bool()
	student_housing = fields.Bool()
	corporate_housing = fields.Bool()
	affordable = fields.Bool()
	luxury = fields.Bool()
	cheap = fields.Bool()
	short_term = fields.Bool()
	# Square Feet
	square_feet_minimum = fields.Str() # No Min, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2500, 3000, 3500, 4000, 4500
	square_feet_maxiumum = fields.Str() # Same as above 	
	
	

	

