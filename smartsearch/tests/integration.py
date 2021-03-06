import unittest
from app import app
import json
import re

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
            self.assertEqual('23221', i['Listing']['Address']['PostalCode']) # Getting 23233 zip codes for some reason

    def testCityStateAndRatingResponse(self):
        result = self.app.get( # Show me all 5 star apartments in Richmond, Virginia
            'http://localhost:5000/nlp?request=Show%20me%20all%205%20star%20apartments%20in%20Richmond%2C%20Virginia%20&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            self.assertEqual(5, i['Listing']['Rating'])

    def testCityStateAndMaxPrice(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia less than $800 per month
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20less%20than%20%24800%20per%20month&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            min_price = int(re.compile("\d+").findall(i['RentFormat']['Rents'].replace(',', ''))[0])
            self.assertLessEqual(min_price, 800)

    def testCityStateAndMinPrice(self):
        result = self.app.get(  # Show me all apartments in Richmond, Virginia greater than $1000 per month
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20greater%20than%20%241000%20per%20month&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            max_price = int(re.compile("\d+").findall(i['RentFormat']['Rents'].replace(',', ''))[-1])
            self.assertGreaterEqual(max_price, 1000)

    def testCityStateAndMaxBed(self):
        result = self.app.get(  # Show me all apartments in Richmond, Virginia with less than 2 bedrooms
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20with%20less%20than%202%20bedrooms&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            min_bed = int(re.compile("\d+").findall(i['RentFormat']['Beds'])[0])
            self.assertLessEqual(min_bed, 2)

    def testCityStateAndMinBed(self):
        result = self.app.get(  # Show me all apartments in Richmond, Virginia with at least 2 bedrooms
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20with%20at%20least%202%20bedrooms&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            max_bed = int(re.compile("\d+").findall(i['RentFormat']['Beds'])[-1])
            self.assertGreaterEqual(max_bed, 2)

    def extractAmenity(self, apartments_code):

        amenity_codes = [
            ['in_unit_washer_and_dryer', 2],
            ['dishwasher', 4],
            ['air_conditioning', 16],
            ['furnished', 128],
            ['fitness_center', 256],
            ['pool', 512],
            ['parking', 65536],
            ['wheelchair_access', 131072],
            ['elevator', 524228],
            ['washer_and_dryer_hookups', 1048576],
            ['laundry_facilities', 2097152],
            ['utilities_included', 4194304],
            ['lofts', 8388608]
        ]

        amenities = []

        for i in reversed(amenity_codes):
            if apartments_code >= i[-1]:
                amenities.append(i[0])
                apartments_code -= i[-1]

        return amenities

    def testCityStateAndHasPool(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia that have a pool
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20that%20have%20a%20pool&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            amenities = self.extractAmenity(i['Listing']['Amenities'])
            self.assertTrue('pool' in amenities)

    def testCityStateAndHasElevator(self):
        result = self.app.get( # Show me all apartments in Richmond, Virginia that have an elevator
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20that%20have%20an%20elevator&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            amenities = self.extractAmenity(i['Listing']['Amenities'])
            self.assertTrue('elevator' in amenities)

    '''
        Dog Friendly                Not an amenity (PetFriendly: 1)
        Cat Friendly                Not an amenity (PetFriendly: 2)
    '''

    def testCityStateandCatFriendly(self):
        result = self.app.get(  # Show me all apartments in Richmond, Virginia that are cat friendly
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20that%20are%20cat%20friendly&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            self.assertTrue(i['Listing']['PetFriendly'] >= 2)

    def testCityStateandCatFriendly(self):
        result = self.app.get(  # Show me all apartments in Richmond, Virginia that are dog friendly
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20that%20are%20dog%20friendly&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
            self.assertTrue(i['Listing']['PetFriendly'] == 0 or i['Listing']['PetFriendly'] == 3)

    '''
    def testCityStateAndMaxSqft(self):
        result = self.app.get(  # Show me all apartments in Richmond, Virginia that are under 60,000 sqft
            'http://localhost:5000/nlp?request=Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%20that%20are%20under%2060%2C000%20sqft&request_type=Apartments')
        data = json.loads(result.data)
        for i in data:
            self.assertEqual('Richmond', i['Listing']['Address']['City'])
            self.assertEqual('VA', i['Listing']['Address']['State'])
    '''

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
