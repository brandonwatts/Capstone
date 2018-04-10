import unittest
import spacy
from smartsearch.models.apartments import apartments
from smartsearch.nlp import parse

nlp = spacy.load('en_core_web_sm')


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
        api = apartments._mapattrs(parse("Show me all 5 star apartments in Richmond, VA."))
        rating_code = api.get('Listing').get('Ratings')
        self.assertEqual(16, rating_code)

    def testDoubleRatingCode(self):
        api = apartments._mapattrs(parse("Show me all 4 star and 5 star apartments in Richmond, VA."))
        rating_code = api.get('Listing').get('Ratings')
        self.assertEqual(8 + 16, rating_code)


class TestStateExtraction(unittest.TestCase):

    def testStateFullName(self):
        api = apartments._mapattrs(parse("Show me all the apartments in Richmond, Virginia."))
        state = api.get('state')
        self.assertEqual(state, "Virginia")

    def testStateAbbreviation(self):
        api = apartments._mapattrs(parse("Show me all the apartments in Richmond, Va."))
        state = api.get('state')
        self.assertEqual(state, "Virginia")

    def testStateWithSpace(self):
        api = apartments._mapattrs(parse("What are all the 3 bedrooms in Providence, Rhode Island"))
        state = api.get('state')
        self.assertEqual(state, "Virginia")

    def testSameCityAsState(self):
        api = apartments._mapattrs(parse("Show me all the 3 bedrooms in New York, New York"))
        state = api.get('state')
        self.assertEqual(state, "New York")


class TestCityExtraction(unittest.TestCase):

    def testStateFullName(self):
        api = apartments._mapattrs(parse("Show me all the apartments in Richmond, Virginia."))
        city = api.get('city')
        self.assertEqual(city, "Richmond")

    def testStateAbbreviation(self):
        api = apartments._mapattrs(parse("What rental property is in Charleston, SC."))
        city = api.get('city')
        self.assertEqual(city, "Charleston")

    def testSimilarCityAsState(self):
        api = apartments._mapattrs(parse("Show me all the 3 bedrooms in New York City, New York"))
        city = api.get('city')
        self.assertEqual(city, "New York City")

    def testSameCityAsState(self):
        api = apartments._mapattrs(parse("Show me all the 3 bedrooms in New York, New York"))
        city = api.get('city')
        self.assertEqual(city, "New York")


class TestZipCodeExtraction(unittest.TestCase):

    def testZipCodeAfterState(self):
        api = apartments._mapattrs(parse("Show me everything in Richmond, Virginia 23221."))
        zip_code = api.get('zip_code')
        self.assertEqual(zip_code, ['23221'])

    def testZipCodeByItself(self):
        api = apartments._mapattrs(parse("List houses in the 23269 area code of Richmond."))
        zip_code = api.get('zip_code')
        self.assertEqual(zip_code, ['23269'])

    def testZipCodeNoState(self):
        api = apartments._mapattrs(parse("List apartments in the 23269 area"))
        zip_code = api.get('zip_code')
        self.assertEqual(zip_code, ['23269'])


class TestMinSqftExtraction(unittest.TestCase):

    def test_min_sqft_1(self):
        api = apartments._mapattrs(parse("Show all 2,000 feet apartments"))
        min_sqft = api.get("min_sqft")
        self.assertEqual(min_sqft, ['2,000'])

    def test_min_sqft_2(self):
        api = apartments._mapattrs(parse("Show all apartments that are greater than 2,000 squarefeet in Richmond"))
        min_sqft = api.get("min_sqft")
        self.assertEqual(min_sqft, ['2,000'])

    def test_min_sqft_3(self):
        api = apartments._mapattrs(parse("Show all apartments that are greater than 2,000 squarefoot in Richmond"))
        min_sqft = api.get("min_sqft")
        self.assertEqual(min_sqft, ['2,000'])

    def test_min_sqft_4(self):
        api = apartments._mapattrs(parse("Show all apartments that are greater than 2,000 sqft in Richmond"))
        min_sqft = api.get("min_sqft")
        self.assertEqual(min_sqft, ['2,000'])

    def test_min_sqft_5(self):
        api = apartments._mapattrs(parse("List apartments with at greater than 1,000 sqft."))
        min_sqft = api.get("min_sqft")
        self.assertEqual(min_sqft, ['1,000'])

    def test_min_sqft_6(self):
        api = apartments._mapattrs(parse("List apartments with at greater than 1,000 sq"))
        min_sqft = api.get("min_sqft")
        self.assertEqual(min_sqft, ['1,000'])

    def test_min_sqft_7(self):
        api = apartments._mapattrs(parse("List apartments with at greater than 1,000 ft"))
        min_sqft = api.get("min_sqft")
        self.assertEqual(min_sqft, ['1,000'])

    def test_min_sqft_8(self):
        api = apartments._mapattrs(parse("Show me all apartments that are at least 50,000 sqft and under 60,000 sqft"))
        min_sqft = api.get("min_sqft")
        self.assertEqual(min_sqft, ['50,000'])


class TestMaxSqftExtraction(unittest.TestCase):

    def test_max_sqft_1(self):
        api = apartments._mapattrs(parse("Show me all apartments that are under 60,000 sqft"))
        max_sqft = api.get("max_sqft")
        self.assertEqual(max_sqft, ['60,000'])

    def test_max_sqft_2(self):
        api = apartments._mapattrs(parse("Show me all apartments that are at least 50,000 sqft and under 60,000 sqft"))
        max_sqft = api.get("max_sqft")
        self.assertEqual(max_sqft, ['60,000'])


class TestMinPriceExtraction(unittest.TestCase):

    def test_min_price_1(self):
        api = apartments._mapattrs(parse("Property in Richmond for 250,000$"))
        min_price = api.get("min_price")
        self.assertEqual(min_price, ['250,000'])

    def test_min_price_2(self):
        api = apartments._mapattrs(parse("List houses in Richmond more than $500,000"))
        min_price = api.get("min_price")
        self.assertEqual(min_price, ['500,000'])

    def test_min_price_3(self):
        api = apartments._mapattrs(parse("List houses in Richmond that are greater than $500,000"))
        min_price = api.get("min_price")
        self.assertEqual(min_price, ['500,000'])

    def test_min_price_4(self):
        api = apartments._mapattrs(parse("List houses in Richmond that are over $500,000"))
        min_price = api.get("min_price")
        self.assertEqual(min_price, ['500,000'])


class TestMaxPriceExtraction(unittest.TestCase):

    def testLessThanPrice(self):
        api = apartments._mapattrs(parse("Show apartments in Richmond, Virginia less than $1,000 per month."))
        max_price = api.get("max_price")
        self.assertEqual(max_price, ['1,000'])

    def testUnderPrice(self):
        api = apartments._mapattrs(parse("I want all apartments in Chicago that are under $1,000 per month."))
        max_price = api.get("max_price")
        self.assertEqual(max_price, ['1,000'])

    def testBelowPrice(self):
        api = apartments._mapattrs(parse("I want all apartments in Chicago that are below $1,000 per month."))
        max_price = api.get("max_price")
        self.assertEqual(max_price, ['1,000'])


class TestMinBedExtraction(unittest.TestCase):

    def testAtLeastNumberOfBedrooms(self):
        api = apartments._mapattrs(parse("List apartments with at least 3 rooms"))
        min_bed = api.get("min_bed")
        self.assertEqual(min_bed, ['3'])

    def testWithSpecificNumberOfBedrooms(self):
        api = apartments._mapattrs(parse("Show all houses with 2 bedrooms"))
        min_bed = api.get("min_bed")
        self.assertEqual(min_bed, ['2'])


class TestMaxBedExtraction(unittest.TestCase):

    def testLessThanNumberOfBedrooms(self):
        api = apartments._mapattrs(parse("Apartments in Richmond with less than 17 bedrooms"))
        max_bed = api.get("max_bed")
        self.assertEqual(max_bed, ['17'])

    def testUnderNumberOfBedrooms(self):
        api = apartments._mapattrs(parse("Apartments in Richmond that have under 17 bedrooms"))
        max_bed = api.get("max_bed")
        self.assertEqual(max_bed, ['17'])


class TestAddressExtraction(unittest.TestCase):

    def testAddressWithCityAndState(self):
        api = apartments._mapattrs(parse("Give me all the apartments near 1300 West Avenue, Richmond, Virginia"))
        address = api.get('max_beds')
        self.assertEqual(address, ['1300', 'West', 'Avenue'])

    def testAddressWithStateNoCity(self):
        api = apartments._mapattrs(parse("Give me all the apartments near 1700 West Highway in Virginia"))
        address = api.get('address')
        self.assertEqual(address, ['1700', 'West', 'Highway'])

    def testRadiusAroundAddress(self):
        api = apartments._mapattrs(parse("Give me all the apartments within 3 miles of 555 Jefferson Road in Virginia"))
        address = api.get('address')
        self.assertEqual(address, ['555', 'Jefferson', 'Road'])


class TestBuildYearExtraction(unittest.TestCase):

    def testBuiltSinceSpecificDate(self):
        api = apartments._mapattrs(parse("Give me all buildings built since 1990"))
        build_year = api.get('build_year')
        self.assertEqual(build_year, ['1990'])


class TestDogFriendlyExtraction(unittest.TestCase):

    def testIsDogFriendly(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that are dog friendly"))
        dog_friendly = api.get('dog_friendly')
        self.assertTrue(dog_friendly)

    def testNotDogFriendly(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that are not dog friendly"))
        dog_friendly = api.get('dog_friendly')
        self.assertFalse(dog_friendly)

    def testDogFriendlyIndirectlyStated(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that love dogs"))
        dog_friendly = api.get('dog_friendly')
        self.assertTrue(dog_friendly)


class TestCatFriendly(unittest.TestCase):

    def testIsCatFriendly(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that are cat friendly"))
        cat_friendly = api.get('cat_friendly')
        self.assertTrue(cat_friendly)

    def testNotCatFriendly(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that are not cat friendly"))
        cat_friendly = api.get('cat_friendly')
        self.assertFalse(cat_friendly)

    def testCatFriendlyIndirectlyStated(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that love cats"))
        cat_friendly = api.get('cat_friendly')
        self.assertTrue(cat_friendly)


class TestHasPoolExtraction(unittest.TestCase):

    def testHasPool(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that have a pool"))
        has_pool = api.get('has_pool')
        self.assertTrue(has_pool)

    def testDoesNotHavePool(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that do not have a pool"))
        has_pool = api.get('has_pool')
        self.assertFalse(has_pool)


class TestHasElevatorExtraction(unittest.TestCase):

    def testHasElevator(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that have an elevator"))
        has_elevator = api.get('has_elevator')
        self.assertTrue(has_elevator)

    def testDoesNotHaveElevator(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that do not have an elevator"))
        has_elevator = api.get('has_elevator')
        self.assertFalse(has_elevator)

    def testHasLift(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that have a lift"))
        has_elevator = api.get('has_elevator')
        self.assertTrue(has_elevator)


class TestFitnessCenterExtraction(unittest.TestCase):

    def testHasFitnessCenter(self):
        api = apartments._mapattrs(
            parse("Show me all buildings in Richmond, Virginia that have a fitness center nearby"))
        has_fitness_center = api.get('has_fitness_center')
        self.assertTrue(has_fitness_center)

    def testDoesNotHaveFitnessCenter(self):
        api = apartments._mapattrs(
            parse("Show me all buildings in Richmond, Virginia that do not have a fitness center nearby"))
        has_fitness_center = api.get('has_fitness_center')
        self.assertFalse(has_fitness_center)

    def testHasGym(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that have a local gym"))
        has_fitness_center = api.get('has_fitness_center')
        self.assertTrue(has_fitness_center)


class TestHasWheelChairAccessExtraction(unittest.TestCase):

    def testHasWheelChairAccess(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that have wheelchair access"))
        has_wheelchair_access = api.get('has_wheelchair_access')
        self.assertTrue(has_wheelchair_access)

    def testDoesNotHaveWheelChairAccess(self):
        api = apartments._mapattrs(
            parse("Show me all buildings in Richmond, Virginia that do not have wheelchair access"))
        has_wheelchair_access = api.get('has_wheelchair_access')
        self.assertFalse(has_wheelchair_access)

    def test_has_wheelchair_access_3(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that have handicap access"))
        has_wheelchair_access = api.get('has_wheelchair_access')
        self.assertTrue(has_wheelchair_access)


class TestHasDishwasherExtraction(unittest.TestCase):

    def testHasDishwasher(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that have a dishwasher"))
        has_dishwasher = api.get('has_dishwasher')
        self.assertTrue(has_dishwasher)

    def testDoesNotHaveDishwasher(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that do not have a dishwasher"))
        has_dishwasher = api.get('has_dishwasher')
        self.assertFalse(has_dishwasher)

    def testDishWasherIndirectlyStated(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that have a dish cleaner"))
        has_dishwasher = api.get('has_dishwasher')
        self.assertTrue(has_dishwasher)


class TestHasAirConditioningExtraction(unittest.TestCase):

    def testHasAirConditioning(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that have air conditioning"))
        has_air_conditioning = api.get("has_air_conditioning")
        self.assertTrue(has_air_conditioning)

    def testDoesNotHaveAirConditioning(self):
        api = apartments._mapattrs(
            parse("Show me all buildings in Richmond, Virginia that does not have air conditioning"))
        has_air_conditioning = api.get("has_air_conditioning")
        self.assertFalse(has_air_conditioning)

    def testAirConditioningIndirectlyStated(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that have heating and cooling"))
        has_air_conditioning = api.get("has_air_conditioning")
        self.assertTrue(has_air_conditioning)


class TestHasParkingExtraction(unittest.TestCase):

    def testHasParking(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that have parking"))
        has_parking = api.get("has_parking")
        self.assertTrue(has_parking)

    def testDoesNotHaveParking(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that do not have parking"))
        has_parking = api.get("has_parking")
        self.assertFalse(has_parking)

    def testHasParkingIndirectlyStated(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that have a parking garage"))
        has_parking = api.get("has_parking")
        self.assertTrue(has_parking)


class TestIsFurnishedExtraction(unittest.TestCase):

    def testIsFurnished(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that are furnished"))
        is_furnished = api.get("is_furnished")
        self.assertTrue(is_furnished)

    def testIsNotFurnished(self):
        api = apartments._mapattrs(parse("Show me all buildings in Richmond, Virginia that are not furnished"))
        is_furnished = api.get("is_furnished")
        self.assertFalse(is_furnished)

    def testIsFurnishedIndirectlyStated(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that already have furniture"))
        is_furnished = api.get("is_furnished")
        self.assertTrue(is_furnished)


class TestHasLaundryFacilitiesExtraction(unittest.TestCase):

    def testHasLaundryFacilities(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that have laundry facilities"))
        has_laundry_facilities = api.get('has_laundry_facilities')
        self.assertEqual(has_laundry_facilities, True)

    def testDoesNotHaveLaundryFacilities(self):
        api = apartments._mapattrs(
            parse("Show me all apartments in Richmond, Virginia that do not have laundry facilities"))
        has_laundry_facilities = api.get('has_laundry_facilities')
        self.assertEqual(has_laundry_facilities, False)

    def testHasLaundryFacilitiesIndirectlyStated(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that have a washing machine"))
        has_laundry_facilities = api.get('has_laundry_facilities')
        self.assertEqual(has_laundry_facilities, True)

    def testHasLaundryFacilitiesIndirectlyStated_2(self):
        api = apartments._mapattrs(parse("Show me all apartments in Richmond, Virginia that have a washer and dryer"))
        has_laundry_facilities = api.get('has_laundry_facilities')
        self.assertEqual(has_laundry_facilities, True)


if __name__ == '__main__':
    unittest.main()
