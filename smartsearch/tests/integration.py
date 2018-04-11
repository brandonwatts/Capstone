import unittest
from app import app
import json


class TestRequestTypeGeneral(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def testCityAndStateWithPeriodResponse(self):
        result = self.app.get('http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia.&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data.get('city'))
        self.assertEqual('VA', data.get('state'))

    def testCityAndStateWithoutPeriodResponse(self):
        result = self.app.get('http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data.get('city'))
        self.assertEqual('VA', data.get('state'))

    def testCityAndStateWithCommaResponse(self):
        result = self.app.get(
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia.&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data.get('city'))
        self.assertEqual('VA', data.get('state'))

    def testCityAndStateWithoutCommaResponse(self):
        result = self.app.get(
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%20Virginia.&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data.get('city'))
        self.assertEqual('VA', data.get('state'))

    def testCityStateAndZipWithPeriodResponse(self):
        result = self.app.get('http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%2023221.&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data.get('city'))
        self.assertEqual('VA', data.get('state'))
        self.assertEqual('23221', data.get('zip_code'))

    def testCityStateAndZipWithoutPeriodResponse(self):
        result = self.app.get('http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%2023221&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data.get('city'))
        self.assertEqual('VA', data.get('state'))
        self.assertEqual('23221', data.get('zip_code'))

    def tearDown(self):
        pass

class TestRequestTypeApartments(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def testRichmondVirginiaWithPeriodResponse(self):
        result = self.app.get(
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia.&request_type=Apartments')
        data = json.loads(result.data)
        self.assertTrue(data.__len__ > 10)

    def testRichmondVirginiaWithoutPeriodResponse(self):
        result = self.app.get(
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia&request_type=Apartments')
        data = json.loads(result.data)
        self.assertTrue(data.__len__ > 10)

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
