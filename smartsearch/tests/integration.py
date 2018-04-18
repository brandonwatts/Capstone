import unittest
from app import app
import json
import re

'''
i['Listing']['Address']['City']
i['Listing']['Address']['State]
i['Listing']['Address']['PostalCode]
i['Listing']['Address']['Amenities'] (int)
i['Listing']['Rating'] (int)

i['RentFormat']['Rents'] = '$1,240 - $2,111'
i['RentFormat']['Beds'] = '1-3 Bed'

Show me all 2,000 squarefeet apartments in Richmond, Virginia
http://127.0.0.1:5000/nlp?request=Show%20me%20all%202%2C000%20squarefeet%20apartments%20in%20Richmond%2C%20Virginia&request_type=Apartments

Show me all apartments in Richmond, Virginia that are under 60,000 sqft
http://127.0.0.1:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20that%20are%20under%2060%2C000%20sqft&request_type=Apartments

Show me all apartments in Richmond, Virginia with at least 2 bedrooms
http://127.0.0.1:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20with%20at%20least%202%20bedrooms&request_type=Apartments

Show me all apartments in Richmond, Virginia with more than 2 bedrooms
http://127.0.0.1:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20with%20more%20than%202%20bedrooms&request_type=Apartments

Show me all apartments in Richmond, Virginia less than $800 per month
http://127.0.0.1:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20less%20than%20%24800%20per%20month&request_type=Apartments

Show me all apartments in Richmond, Virginia greater than $1000 per month
http://127.0.0.1:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20greater%20than%20%241000%20per%20month&request_type=Apartments

Show me all 5 star apartments in Richmond, Virginia 
http://127.0.0.1:5000/nlp?request=Show%20me%20all%205%20star%20apartments%20in%20Richmond%2C%20Virginia%20&request_type=Apartments
'''

class TestRequestTypeGeneral(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def testCityAndStateWithPeriodResponse(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia.
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia.&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data['city'])
        self.assertEqual('Virginia', data['state'])

    def testCityAndStateWithoutPeriodResponse(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data['city'])
        self.assertEqual('Virginia', data['state'])

    def testCityAndStateWithCommaResponse(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia.
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia.&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data['city'])
        self.assertEqual('Virginia', data['state'])

    def testCityAndStateWithoutCommaResponse(self):
        result = self.app.get( # Show me all apartments in Richmond Virginia.
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%20Virginia.&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data['city'])
        self.assertEqual('Virginia', data['state'])

    def testCityStateAndZipWithPeriodResponse(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia 23221.
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%2023221.&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data['city'])
        self.assertEqual('Virginia', data['state'])
        self.assertEqual('23221', data['zip_code'])

    def testCityStateAndZipWithoutPeriodResponse(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia 23221
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%2023221&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data['city'])
        self.assertEqual('Virginia', data['state'])
        self.assertEqual('23221', data['zip_code'])

    def tearDown(self):
        pass

class TestRequestTypeApartments(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def testCityAndStateResponse(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])

    def testCityStateAndZipCodeResponse(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia, 23221
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%2023221&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            self.assertEqual('23221', i['Listing']['Address']['PostalCode'])

    def testCityStateAndRatingResponse(self):
        result = self.app.get( # Show me all 5 star apartments in Richmond, Virginia
            'http://localhost:5000/nlp?request=Show%20me%20all%205%20star%20apartments%20in%20Richmond%2C%20Virginia%20&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            self.assertEqual(5, i['Listing']['Rating'])

    def testCityStateAndMaxRent(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia less than $800 per month
            'http://localhost:5000/nlp?request=Show%20me%20all%205%20star%20apartments%20in%20Richmond%2C%20Virginia%20&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])

            # Format of Rent is '$1,240 - $2,111'
            # I match the two numbers, grab the last match, remove the comma, and then cast to int
            #regex = re.compile("\d+(,\d+)*")
            #regex = re.compile("((\d+,\d+)|\d+)")
            #bob = regex.findall(i['RentFormat']['Rents'])
            #c = int(regex.findall(i['RentFormat']['Rents'])[-1][-1].replace(',', ''))
            #self.assertLessEqual(800, c)

    def tearDown(self):
        pass

""" - This is more of an integration test
class TestMapAmenities(unittest.TestCase):

    def testSingleAmenityCode(self):
        api = apartments._mapattrs(parse("Show me all apartments that have a pool in Richmond, VA."))
        amenity_code = api.get('Listing').get('Amenities')
        self.assertEqual(512, amenity_code)

    def testMultipleAmenitiesCode(self):
        api = apartments._mapattrs(
            parse("Show me all apartments that have a pool and a dishwasher in Richmond, VA."))
        amenity_code = api.get('Listing').get('Amenities')
        self.assertEqual(512 + 4, amenity_code)
        
class TestMapRatings(unittest.TestCase):

    def testSingleRatingCode(self):
        api = parse("Show me all 5 star apartments in Richmond, VA.")
        rating_code = api.get('Listing').get('Ratings')
        self.assertEqual(16, rating_code)

    def testDoubleRatingCode(self):
        api = parse("Show me all 4 star and 5 star apartments in Richmond, VA.")
        rating_code = api.get('Listing').get('Ratings')
        self.assertEqual(8 + 16, rating_code)
        
"""


if __name__ == '__main__':
    unittest.main()
