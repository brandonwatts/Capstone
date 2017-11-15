"""APIResponse.py is the response the the api/nlp endpoint"""

__author__ = "Brandon Watts"
__credits__ = ['Jonathan Cary', 'Austin Green']
__license__ = 'MIT'
__version__ = '0.1'


class ApiResponse(object):
    def __init__(self, states, city, zip_code, sq_ft, price):
        self.states = states
        self.city = city
        self.zip_code = zip_code
        self.sq_ft = sq_ft
        self.price = price
