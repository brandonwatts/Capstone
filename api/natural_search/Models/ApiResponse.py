"""APIResponse.py is the response the the api/nlp endpoint"""

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'


class ApiResponse(object):
    def __init__(self, state, city, zip_code, min_sqft, max_sqft, min_price, max_price, min_bed, max_bed, pricing_type,
                 address, build_date):
        self.state = state
        self.city = city
        self.zip_code = zip_code
        self.min_sqft = min_sqft
        self.max_sqft = max_sqft
        self.min_price = min_price
        self.max_price = max_price
        self.min_bed = min_bed,
        self.max_bed = max_bed,
        self.pricing_type = pricing_type
        self.address = address
        self.build_date = build_date
