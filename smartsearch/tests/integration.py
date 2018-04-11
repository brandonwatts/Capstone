import unittest
from app import app
import json


class TestRequestTypeGeneral(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def testSimpleNlpResponse(self):
        result = self.app.get('http://localhost:5000/nlp?request=%22Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%22&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data.get('city'))
        self.assertEqual('VA', data.get('state'))

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
