import unittest
import spacy
from smartsearch.nlp import parse

nlp = spacy.load('en_core_web_sm')


class TestStateExtraction(unittest.TestCase):

    def testStateFullName(self):
        api = parse("Show me all the apartments in Richmond, Virginia.")
        self.assertEqual(api['state'], "Virginia")

    def testStateAbbreviation(self):
        api = parse("Show me all the apartments in Richmond, Va.")
        self.assertEqual(api['state'], "Virginia")

    def testStateWithSpace(self):
        api = parse("What are all the 3 bedrooms in Providence, Rhode Island")
        self.assertEqual(api['state'], "Rhode Island")

    def testSameCityAsState(self):
        api = parse("Show me all the 3 bedrooms in New York, New York")
        self.assertEqual(api['state'], "New York")


class TestCityExtraction(unittest.TestCase):

    def testStateFullName(self):
        api = parse("Show me all the apartments in Richmond, Virginia.")
        self.assertEqual(api["city"], "Richmond")

    def testStateAbbreviation(self):
        api = parse("What rental property is in Charleston, SC.")
        self.assertEqual(api["city"], "Charleston")

    def testSimilarCityAsState(self):
        api = parse("Show me all the 3 bedrooms in New York City, New York")
        self.assertEqual(api["city"], "New York City")

    def testSameCityAsState(self):
        api = parse("Show me all the 3 bedrooms in New York, New York")
        self.assertEqual(api["city"], "New York")


class TestZipCodeExtraction(unittest.TestCase):

    def testZipCodeAfterState(self):
        api = parse("Show me everything in Richmond, Virginia 23221.")
        self.assertEqual(api['zip_code'], '23221')

    def testZipCodeByItself(self):
        api = parse("List houses in the 23269 area code of Richmond.")
        self.assertEqual(api['zip_code'], '23269')

    def testZipCodeNoState(self):
        api = parse("List apartments in the 23269 area")
        self.assertEqual(api['zip_code'], '23269')


class TestMinSqftExtraction(unittest.TestCase):

    def test_min_sqft_1(self):
        api = parse("Show all 2,000 feet apartments")
        self.assertEqual(api['min_sqft'], '2000')

    def test_min_sqft_2(self):
        api = parse("Show all apartments that are greater than 2,000 squarefeet in Richmond")
        self.assertEqual(api['min_sqft'], '2000')

    def test_min_sqft_3(self):
        api = parse("Show all apartments that are greater than 2,000 squarefoot in Richmond")
        self.assertEqual(api['min_sqft'], '2000')

    def test_min_sqft_4(self):
        api = parse("Show all apartments that are greater than 2,000 sqft in Richmond")
        self.assertEqual(api['min_sqft'], '2000')

    def test_min_sqft_5(self):
        api = parse("List apartments with at greater than 1,000 sqft.")
        self.assertEqual(api['min_sqft'], '1000')

    def test_min_sqft_6(self):
        api = parse("List apartments with at greater than 1,000 sq")
        self.assertEqual(api['min_sqft'], '1000')

    def test_min_sqft_7(self):
        api = parse("List apartments with at greater than 1,000 ft")
        self.assertEqual(api['min_sqft'], '1000')

    def test_min_sqft_8(self):
        api = parse("Show me all apartments that are at least 50,000 sqft and under 60,000 sqft")
        self.assertEqual(api['min_sqft'], '50000')


class TestMaxSqftExtraction(unittest.TestCase):

    def test_max_sqft_1(self):
        api = parse("Show me all apartments that are under 60,000 sqft")
        max_sqft = api.get("max_sqft")
        self.assertEqual(max_sqft, '60000')

    def test_max_sqft_2(self):
        api = parse("Show me all apartments that are at least 50,000 sqft and under 60,000 sqft")
        max_sqft = api.get("max_sqft")
        self.assertEqual(max_sqft, '60000')


class TestMinPriceExtraction(unittest.TestCase):

    def testMoreThanPrice(self):
        api = parse("List houses in Richmond more than $500,000")
        min_price = api.get("min_price")
        self.assertEqual(min_price, "500000")

    def testGreaterThanPrice(self):
        api = parse("List houses in Richmond that are greater than $500,000")
        min_price = api.get("min_price")
        self.assertEqual(min_price, '500000')

    def testOverPrice(self):
        api = parse("List houses in Richmond that are over $500,000")
        min_price = api.get("min_price")
        self.assertEqual(min_price, '500000')


class TestMaxPriceExtraction(unittest.TestCase):

    def testLessThanPrice(self):
        api = parse("Show apartments in Richmond, Virginia less than $1,000 per month.")
        max_price = api.get("max_price")
        self.assertEqual(max_price, '1000')

    def testUnderPrice(self):
        api = parse("I want all apartments in Chicago that are under $1,000 per month.")
        max_price = api.get("max_price")
        self.assertEqual(max_price, '1000')

    def testBelowPrice(self):
        api = parse("I want all apartments in Chicago that are below $1,000 per month.")
        max_price = api.get("max_price")
        self.assertEqual(max_price, '1000')


class TestMinBedExtraction(unittest.TestCase):

    def testAtLeastNumberOfBedrooms(self):
        api = parse("List apartments with at least 3 rooms")
        self.assertEqual(api['min_bed'], '3')

    def testWithSpecificNumberOfBedrooms(self):
        api = parse("Show all houses with 2 bedrooms")
        self.assertEqual(api['min_bed'], '2')


class TestMaxBedExtraction(unittest.TestCase):

    def testLessThanNumberOfBedrooms(self):
        api = parse("Apartments in Richmond with less than 17 bedrooms")
        self.assertEqual(api['max_bed'], '17')

    def testUnderNumberOfBedrooms(self):
        api = parse("Apartments in Richmond that have under 17 bedrooms")
        self.assertEqual(api['max_bed'], '17')


class TestAddressExtraction(unittest.TestCase):

    def testAddressWithCityAndState(self):
        api = parse("Give me all the apartments near 1300 West Avenue, Richmond, Virginia")
        self.assertEqual(api['address'], '1300 West Avenue')

    def testAddressWithStateNoCity(self):
        api = parse("Give me all the apartments near 1700 West Highway in Virginia")
        self.assertEqual(api['address'], '1700 West Highway')

    def testRadiusAroundAddress(self):
        api = parse("Give me all the apartments within 3 miles of 555 Jefferson Road in Virginia")
        self.assertEqual(api['address'], '555 Jefferson Road')


class TestBuildYearExtraction(unittest.TestCase):

    def testBuiltSinceSpecificDate(self):
        api = parse("Give me all buildings built since 1990")
        self.assertEqual(api['build_year'], '1990')


class TestDogFriendlyExtraction(unittest.TestCase):

    def testIsDogFriendly(self):
        api = parse("Show me all apartments in Richmond, Virginia that are dog friendly")
        dog_friendly = api.get('dog_friendly')
        self.assertTrue(dog_friendly)

    def testNotDogFriendly(self):
        api = parse("Show me all apartments in Richmond, Virginia that are not dog friendly")
        dog_friendly = api.get('dog_friendly')
        self.assertFalse(dog_friendly)

    def testDogFriendlyIndirectlyStated(self):
        api = parse("Show me all apartments in Richmond, Virginia that love dogs")
        dog_friendly = api.get('dog_friendly')
        self.assertTrue(dog_friendly)


class TestCatFriendly(unittest.TestCase):

    def testIsCatFriendly(self):
        api = parse("Show me all apartments in Richmond, Virginia that are cat friendly")
        cat_friendly = api.get('cat_friendly')
        self.assertTrue(cat_friendly)

    def testNotCatFriendly(self):
        api = parse("Show me all apartments in Richmond, Virginia that are not cat friendly")
        cat_friendly = api.get('cat_friendly')
        self.assertFalse(cat_friendly)

    def testCatFriendlyIndirectlyStated(self):
        api = parse("Show me all apartments in Richmond, Virginia that love cats")
        cat_friendly = api.get('cat_friendly')
        self.assertTrue(cat_friendly)


class TestHasPoolExtraction(unittest.TestCase):

    def testHasPool(self):
        api = parse("Show me all apartments in Richmond, Virginia that have a pool")
        has_pool = api.get('has_pool')
        self.assertTrue(has_pool)

    def testDoesNotHavePool(self):
        api = parse("Show me all apartments in Richmond, Virginia that do not have a pool")
        has_pool = api.get('has_pool')
        self.assertFalse(has_pool)


class TestHasElevatorExtraction(unittest.TestCase):

    def testHasElevator(self):
        api = parse("Show me all buildings in Richmond, Virginia that have an elevator")
        has_elevator = api.get('has_elevator')
        self.assertTrue(has_elevator)

    def testDoesNotHaveElevator(self):
        api = parse("Show me all buildings in Richmond, Virginia that do not have an elevator")
        has_elevator = api.get('has_elevator')
        self.assertFalse(has_elevator)

    def testHasLift(self):
        api = parse("Show me all buildings in Richmond, Virginia that have a lift")
        has_elevator = api.get('has_elevator')
        self.assertTrue(has_elevator)


class TestFitnessCenterExtraction(unittest.TestCase):

    def testHasFitnessCenter(self):
        api = parse("Show me all buildings in Richmond, Virginia that have a fitness center nearby")
        has_fitness_center = api.get('has_fitness_center')
        self.assertTrue(has_fitness_center)

    def testDoesNotHaveFitnessCenter(self):
        api = parse("Show me all buildings in Richmond, Virginia that do not have a fitness center nearby")
        has_fitness_center = api.get('has_fitness_center')
        self.assertFalse(has_fitness_center)

    def testHasGym(self):
        api = parse("Show me all buildings in Richmond, Virginia that have a local gym")
        has_fitness_center = api.get('has_fitness_center')
        self.assertTrue(has_fitness_center)


class TestHasWheelChairAccessExtraction(unittest.TestCase):

    def testHasWheelChairAccess(self):
        api = parse("Show me all buildings in Richmond, Virginia that have wheelchair access")
        has_wheelchair_access = api.get('has_wheelchair_access')
        self.assertTrue(has_wheelchair_access)

    def testDoesNotHaveWheelChairAccess(self):
        api = parse("Show me all buildings in Richmond, Virginia that do not have wheelchair access")
        has_wheelchair_access = api.get('has_wheelchair_access')
        self.assertFalse(has_wheelchair_access)

    def test_has_wheelchair_access_3(self):
        api = parse("Show me all buildings in Richmond, Virginia that have handicap access")
        has_wheelchair_access = api.get('has_wheelchair_access')
        self.assertTrue(has_wheelchair_access)


class TestHasDishwasherExtraction(unittest.TestCase):

    def testHasDishwasher(self):
        api = parse("Show me all buildings in Richmond, Virginia that have a dishwasher")
        has_dishwasher = api.get('has_dishwasher')
        self.assertTrue(has_dishwasher)

    def testDoesNotHaveDishwasher(self):
        api = parse("Show me all buildings in Richmond, Virginia that do not have a dishwasher")
        has_dishwasher = api.get('has_dishwasher')
        self.assertFalse(has_dishwasher)

    def testDishWasherIndirectlyStated(self):
        api = parse("Show me all apartments in Richmond, Virginia that have a dish cleaner")
        has_dishwasher = api.get('has_dishwasher')
        self.assertTrue(has_dishwasher)


class TestHasAirConditioningExtraction(unittest.TestCase):

    def testHasAirConditioning(self):
        api = parse("Show me all buildings in Richmond, Virginia that have air conditioning")
        has_air_conditioning = api.get("has_air_conditioning")
        self.assertTrue(has_air_conditioning)

    def testDoesNotHaveAirConditioning(self):
        api = parse("Show me all buildings in Richmond, Virginia that does not have air conditioning")
        has_air_conditioning = api.get("has_air_conditioning")
        self.assertFalse(has_air_conditioning)

    def testAirConditioningIndirectlyStated(self):
        api = parse("Show me all apartments in Richmond, Virginia that have heating and cooling")
        has_air_conditioning = api.get("has_air_conditioning")
        self.assertTrue(has_air_conditioning)


class TestHasParkingExtraction(unittest.TestCase):

    def testHasParking(self):
        api = parse("Show me all buildings in Richmond, Virginia that have parking")
        has_parking = api.get("has_parking")
        self.assertTrue(has_parking)

    def testDoesNotHaveParking(self):
        api = parse("Show me all buildings in Richmond, Virginia that do not have parking")
        has_parking = api.get("has_parking")
        self.assertFalse(has_parking)

    def testHasParkingIndirectlyStated(self):
        api = parse("Show me all apartments in Richmond, Virginia that have a parking garage")
        has_parking = api.get("has_parking")
        self.assertTrue(has_parking)


class TestIsFurnishedExtraction(unittest.TestCase):

    def testIsFurnished(self):
        api = parse("Show me all buildings in Richmond, Virginia that are furnished")
        is_furnished = api.get("is_furnished")
        self.assertTrue(is_furnished)

    def testIsNotFurnished(self):
        api = parse("Show me all buildings in Richmond, Virginia that are not furnished")
        is_furnished = api.get("is_furnished")
        self.assertFalse(is_furnished)

    def testIsFurnishedIndirectlyStated(self):
        api = parse("Show me all apartments in Richmond, Virginia that already have furniture")
        is_furnished = api.get("is_furnished")
        self.assertTrue(is_furnished)


class TestHasLaundryFacilitiesExtraction(unittest.TestCase):

    def testHasLaundryFacilities(self):
        api = parse("Show me all apartments in Richmond, Virginia that have laundry facilities")
        has_laundry_facilities = api.get('has_laundry_facilities')
        self.assertEqual(has_laundry_facilities, True)

    def testDoesNotHaveLaundryFacilities(self):
        api = parse("Show me all apartments in Richmond, Virginia that do not have laundry facilities")
        has_laundry_facilities = api.get('has_laundry_facilities')
        self.assertEqual(has_laundry_facilities, False)

    def testHasLaundryFacilitiesIndirectlyStated(self):
        api = parse("Show me all apartments in Richmond, Virginia that have a washing machine")
        has_laundry_facilities = api.get('has_laundry_facilities')
        self.assertEqual(has_laundry_facilities, True)

    def testHasLaundryFacilitiesIndirectlyStated_2(self):
        api = parse("Show me all apartments in Richmond, Virginia that have a washer and dryer")
        has_laundry_facilities = api.get('has_laundry_facilities')
        self.assertEqual(has_laundry_facilities, True)


if __name__ == '__main__':
    unittest.main()
