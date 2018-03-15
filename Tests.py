import unittest
import spacy
from Api.NLP import NLP

nlp_class = NLP()
nlp = spacy.load('en')


class TestStateExtraction(unittest.TestCase):

    def testStateFullName(self):
        doc = nlp("Show me all the apartments in Richmond, Virginia.")
        state = nlp_class.extract_state(doc)
        self.assertEqual(state, "VA")

    def testStateAbbreviation(self):
        doc = nlp("Show me all the apartments in Richmond, Va.")
        state = nlp_class.extract_state(doc)
        self.assertEqual(state, "VA")

    def testStateWithSpace(self):
        doc = nlp("What are all the 3 bedrooms in Providence, Rhode Island")
        state = nlp_class.extract_state(doc)
        self.assertEqual(state, "RI")

    def testSameCityAsState(self):
        doc = nlp("Show me all the 3 bedrooms in New York, New York")
        state = nlp_class.extract_state(doc)
        self.assertEqual(state, "NY")


class TestCityExtraction(unittest.TestCase):

    def testStateFullName(self):
        doc = nlp("Show me all the apartments in Richmond, Virginia.")
        city = nlp_class.extract_city(doc)
        self.assertEqual(city, "Richmond")

    def testStateAbbreviation(self):
        doc = nlp("What rental property is in Charleston, SC.")
        city = nlp_class.extract_city(doc)
        self.assertEqual(city, "Charleston")

    def testSimilarCityAsState(self):
        doc = nlp("Show me all the 3 bedrooms in New York City, New York")
        city = nlp_class.extract_city(doc)
        self.assertEqual(city, "New York City")

    def testSameCityAsState(self):
        doc = nlp("Show me all the 3 bedrooms in New York, New York")
        city = nlp_class.extract_city(doc)
        self.assertEqual(city, "New York")


class TestZipCodeExtraction(unittest.TestCase):

    def testZipCodeAfterState(self):
        doc = nlp("Show me everything in Richmond, Virginia 23221.")
        zip_code = nlp_class.extract_zip_code(doc)
        self.assertEqual(zip_code, ['23221'])

    def testZipCodeByItself(self):
        doc = nlp("List houses in the 23269 area code of Richmond.")
        zip_code = nlp_class.extract_zip_code(doc)
        self.assertEqual(zip_code, ['23269'])


class TestMinSqftExtraction(unittest.TestCase):
    pass
    '''
    def test_min_sqft_1(self):
        doc = nlp("Show all 2,000 feet apartments")
        min_sqft = nlp_class.extract_min_sqft(doc)
        self.assertEqual(min_sqft, ['2,000'])

    def test_min_sqft_2(self):
        doc = nlp("Show all apartments that are greater than 2,000 squarefeet in Richmond")
        min_sqft = nlp_class.extract_min_sqft(doc)
        self.assertEqual(min_sqft, ['2,000'])

    def test_min_sqft_3(self):
        doc = nlp("Show all apartments that are greater than 2,000 squarefoot in Richmond")
        min_sqft = nlp_class.extract_min_sqft(nlp_class, doc)
        self.assertEqual(min_sqft, ['2,000'])

    def test_min_sqft_4(self):
        doc = nlp("Show all apartments that are greater than 2,000 sqft in Richmond")
        min_sqft = nlp_class.extract_min_sqft(nlp_class, doc)
        self.assertEqual(min_sqft, ['2,000'])

    def test_min_sqft_5(self):
        doc = nlp("List apartments with at greater than 1,000 sqft.")
        min_sqft = nlp_class.extract_min_sqft(nlp_class, doc)
        self.assertEqual(min_sqft, ['1,000'])

    def test_min_sqft_6(self):
        doc = nlp("List apartments with at greater than 1,000 sq")
        min_sqft = nlp_class.extract_min_sqft(nlp_class, doc)
        self.assertEqual(min_sqft, ['1,000'])

    def test_min_sqft_7(self):
        doc = nlp("List apartments with at greater than 1,000 ft")
        min_sqft = nlp_class.extract_min_sqft(nlp_class, doc)
        self.assertEqual(min_sqft, ['1,000'])

    def test_min_sqft_8(self):
        doc = nlp("Show me all apartments that are at least 50,000 sqft and under 60,000 sqft")
        min_sqft = nlp_class.extract_min_sqft(nlp_class, doc)
        self.assertEqual(min_sqft, ['50,000'])
'''


class TestMaxSqftExtraction(unittest.TestCase):
    pass
    '''
    def test_max_sqft_1(self):
        doc = nlp("Show me all apartments that are under 60,000 sqft")
        max_sqft = nlp_class.extract_max_sqft(nlp_class, doc)
        self.assertEqual(max_sqft, ['60,000'])

    def test_max_sqft_2(self):
        doc = nlp("Show me all apartments that are at least 50,000 sqft and under 60,000 sqft")
        max_sqft = nlp_class.extract_max_sqft(nlp_class, doc)
        self.assertEqual(max_sqft, ['60,000'])
    '''


class TestMinPriceExtraction(unittest.TestCase):
    pass
    '''
    def test_min_price_1(self):
        doc = nlp("Property in Richmond for 250,000$")
        min_price = nlp_class.extract_min_price(nlp_class, doc)
        self.assertEqual(min_price, ['250,000'])

    def test_min_price_2(self):
        doc = nlp("List houses in Richmond more than $500,000")
        min_price = nlp_class.extract_min_price(nlp_class, doc)
        self.assertEqual(min_price, ['500,000'])

    def test_min_price_3(self):
        doc = nlp("List houses in Richmond that are greater than $500,000")
        min_price = nlp_class.extract_min_price(nlp_class, doc)
        self.assertEqual(min_price, ['500,000'])

    def test_min_price_4(self):
        doc = nlp("List houses in Richmond that are over $500,000")
        min_price = nlp_class.extract_min_price(nlp_class, doc)
        self.assertEqual(min_price, ['500,000'])
    '''


class TestMaxPriceExtraction(unittest.TestCase):
    pass
    '''
    def testLessThanPrice(self):
        doc = nlp("Show apartments in Richmond, Virginia less than $1,000 per month.")
        max_price = nlp_class.extract_max_price(nlp_class, doc)
        self.assertEqual(max_price, ['1,000'])

    def testUnderPrice(self):
        doc = nlp("I want all apartments in Chicago that are under $1,000 per month.")
        max_price = nlp_class.extract_max_price(nlp_class, doc)
        self.assertEqual(max_price, ['1,000'])

    def testBelowPrice(self):
        doc = nlp("I want all apartments in Chicago that are below $1,000 per month.")
        max_price = nlp_class.extract_max_price(nlp_class, doc)
        self.assertEqual(max_price, ['1,000'])
    '''


class TestMinBedExtraction(unittest.TestCase):
    pass
    '''
    def testAtLeastNumberOfBedrooms(self):
        doc = nlp("List apartments with at least 3 rooms")
        min_bed = nlp_class.extract_min_bed(nlp_class, doc)
        self.assertEqual(min_bed, ['3'])

    def testWithSpecificNumberOfBedrooms(self):
        doc = nlp("Show all houses with 2 bedrooms")
        min_bed = nlp_class.extract_min_bed(nlp_class, doc)
        self.assertEqual(min_bed, ['2'])
    '''


class TestMaxBedExtraction(unittest.TestCase):
    pass
    '''
    def testLessThanNumberOfBedrooms(self):
        doc = nlp("Apartments in Richmond with less than 17 bedrooms")
        max_bed = nlp_class.extract_max_bed(nlp_class, doc)
        self.assertEqual(max_bed, ['17'])

    def testUnderNumberOfBedrooms(self):
        doc = nlp("Apartments in Richmond that have under 17 bedrooms")
        max_bed = nlp_class.extract_max_bed(nlp_class, doc)
        self.assertEqual(max_bed, ['17'])
    '''


class TestPricingTypeExtraction(unittest.TestCase):
    pass
    '''
    def testPerMonth(self):
        doc = nlp("Show apartments in Richmond, Virginia less than $1,000 per month.")
        pricing_type = nlp_class.extract_pricing_type(nlp_class, doc)
        self.assertEqual(pricing_type, ['month'])

    def testPerUnit(self):
        doc = nlp("List every apartment less than $100,000 per unit?")
        pricing_type = nlp_class.extract_pricing_type(nlp_class, doc)
        self.assertEqual(pricing_type, ['unit'])
    '''


class TestAddressExtraction(unittest.TestCase):

    def testAddressWithCityAndState(self):
        doc = nlp("Give me all the apartments near 1300 West Avenue, Richmond, Virginia")
        address = nlp_class.extract_address(doc)
        self.assertEqual(address, ['1300', 'West', 'Avenue'])

    def testAddressWithStateNoCity(self):
        doc = nlp("Give me all the apartments near 1700 West Highway in Virginia")
        address = nlp_class.extract_address(doc)
        self.assertEqual(address, ['1700', 'West', 'Highway'])

    def testRadiusAroundAddress(self):
        doc = nlp("Give me all the apartments within 3 miles of 555 Jefferson Road in Virginia")
        address = nlp_class.extract_address(doc)
        self.assertEqual(address, ['555', 'Jefferson', 'Road'])


class TestBuildYearExtraction(unittest.TestCase):

    def testBuiltSinceSpecificDate(self):
        doc = nlp("Give me all buildings built since 1990")
        build_year = nlp_class.extract_address(doc)
        self.assertEqual(build_year, ['1990'])


class TestDogFriendlyExtraction(unittest.TestCase):

    def testIsDogFriendly(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that are dog friendly")
        dog_friendly = nlp_class.extract_dog_friendly(doc)
        self.assertTrue(dog_friendly)

    def testNotDogFriendly(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that are not dog friendly")
        dog_friendly = nlp_class.extract_dog_friendly(doc)
        self.assertFalse(dog_friendly)

    def testDogFriendlyIndirectlyStated(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that love dogs")
        dog_friendly = nlp_class.extract_dog_friendly(doc)
        self.assertTrue(dog_friendly)


class TestCatFriendly(unittest.TestCase):

    def testIsCatFriendly(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that are cat friendly")
        cat_friendly = nlp_class.extract_cat_friendly(doc)
        self.assertTrue(cat_friendly)

    def testNotCatFriendly(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that are not cat friendly")
        cat_friendly = nlp_class.extract_cat_friendly(doc)
        self.assertFalse(cat_friendly)

    def testCatFriendlyIndirectlyStated(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that love cats")
        cat_friendly = nlp_class.extract_cat_friendly(doc)
        self.assertTrue(cat_friendly)


class TestHasPoolExtraction(unittest.TestCase):

    def testHasPool(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that have a pool")
        has_pool = nlp_class.extract_has_pool(doc)
        self.assertTrue(has_pool)

    def testDoesNotHavePool(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that do not have a pool")
        has_pool = nlp_class.extract_has_pool(doc)
        self.assertFalse(has_pool)


class TestHasElevatorExtraction(unittest.TestCase):

    def testHasElevator(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that have an elevator")
        has_elevator = nlp_class.extract_has_elevator(doc)
        self.assertTrue(has_elevator)

    def testDoesNotHaveElevator(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that do not have an elevator")
        has_elevator = nlp_class.extract_has_elevator(doc)
        self.assertFalse(has_elevator)

    def testHasLift(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that have a lift")
        has_elevator = nlp_class.extract_has_elevator(doc)
        self.assertTrue(has_elevator)


class TestFitnessCenterExtraction(unittest.TestCase):

    def testHasFitnessCenter(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that have a fitness center nearby")
        has_fitness_center = nlp_class.extract_has_fitness_center(doc)
        self.assertTrue(has_fitness_center)

    def testDoesNotHaveFitnessCenter(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that do not have a fitness center nearby")
        has_fitness_center = nlp_class.extract_has_fitness_center(doc)
        self.assertFalse(has_fitness_center)

    def testHasGym(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that have a local gym")
        has_fitness_center = nlp_class.extract_has_fitness_center(doc)
        self.assertTrue(has_fitness_center)


class TestHasWheelChairAccessExtraction(unittest.TestCase):

    def testHasWheelChairAccess(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that have wheelchair access")
        has_wheelchair_access = nlp_class.extract_has_wheelchair_access(doc)
        self.assertTrue(has_wheelchair_access)

    def testDoesNotHaveWheelChairAccess(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that do not have wheelchair access")
        has_wheelchair_access = nlp_class.extract_has_wheelchair_access(doc)
        self.assertFalse(has_wheelchair_access)

    def test_has_wheelchair_access_3(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that have handicap access")
        has_wheelchair_access = nlp_class.extract_has_wheelchair_access(doc)
        self.assertTrue(has_wheelchair_access)


class TestHasDishwasherExtraction(unittest.TestCase):

    def testHasDishwasher(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that have a dishwasher")
        has_dishwasher = nlp_class.extract_has_dishwasher(doc)
        self.assertTrue(has_dishwasher)

    def testDoesNotHaveDishwasher(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that do not have a dishwasher")
        has_dishwasher = nlp_class.extract_has_dishwasher(doc)
        self.assertFalse(has_dishwasher)

    def testDishWasherIndirectlyStated(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that have a dish cleaner")
        has_dishwasher = nlp_class.extract_has_dishwasher(doc)
        self.assertTrue(has_dishwasher)


class TestHasAirConditioningExtraction(unittest.TestCase):

    def testHasAirConditioning(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that have air conditioning")
        has_air_conditioning = nlp_class.extract_has_air_conditioning(doc)
        self.assertTrue(has_air_conditioning)

    def testDoesNotHaveAirConditioning(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that does not have air conditioning")
        has_air_conditioning = nlp_class.extract_has_air_conditioning(doc)
        self.assertFalse(has_air_conditioning)

    def testAirConditioningIndirectlyStated(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that have heating and cooling")
        has_air_conditioning = nlp_class.extract_has_air_conditioning(doc)
        self.assertTrue(has_air_conditioning)


class TestHasParkingExtraction(unittest.TestCase):

    def testHasParking(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that have parking")
        has_parking = nlp_class.extract_has_parking(doc)
        self.assertTrue(has_parking)

    def testDoesNotHaveParking(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that do not have parking")
        has_parking = nlp_class.extract_has_parking(doc)
        self.assertFalse(has_parking)

    def testHasParkingIndirectlyStated(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that have a parking garage")
        has_parking = nlp_class.extract_has_parking(doc)
        self.assertTrue(has_parking)


class TestIsFurnishedExtraction(unittest.TestCase):

    def testIsFurnished(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that are furnished")
        is_furnished = nlp_class.extract_is_furnished(doc)
        self.assertTrue(is_furnished)

    def testIsNotFurnished(self):
        doc = nlp("Show me all buildings in Richmond, Virginia that are not furnished")
        is_furnished = nlp_class.extract_is_furnished(doc)
        self.assertFalse(is_furnished)

    def testIsFurnishedIndirectlyStated(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that already have furniture")
        is_furnished = nlp_class.extract_is_furnished(doc)
        self.assertTrue(is_furnished)


class TestHasLaundryFacilitiesExtraction(unittest.TestCase):

    def testHasLaundryFacilities(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that have laundry facilities")
        has_laundry_facilities = nlp_class.extract_has_laundry_facilities(doc)
        self.assertEqual(has_laundry_facilities, True)

    def testDoesNotHaveLaundryFacilities(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that do not have laundry facilities")
        has_laundry_facilities = nlp_class.extract_has_laundry_facilities(doc)
        self.assertEqual(has_laundry_facilities, False)

    def testHasLaundryFacilitiesIndirectlyStated(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that have a washing machine")
        has_laundry_facilities = nlp_class.extract_has_laundry_facilities(doc)
        self.assertEqual(has_laundry_facilities, True)

    def testHasLaundryFacilitiesIndirectlyStated_2(self):
        doc = nlp("Show me all apartments in Richmond, Virginia that have a washer and dryer")
        has_laundry_facilities = nlp_class.extract_has_laundry_facilities(doc)
        self.assertEqual(has_laundry_facilities, True)


class TestPropertyTypeExtraction(unittest.TestCase):

    pass
    '''
    def testIndustrialPropertyType(self):
        doc = nlp("Show me all industrial buildings in Richmond, Virginia")
        property_type = nlp_class.extract_property_type(nlp_class, doc)
        self.assertEqual(property_type, "pt_industrial")

    def testRetailPropertyType(self):
        doc = nlp("Show me all non-retail buildings in Richmond, Virginia")
        property_type = nlp_class.extract_property_type(nlp_class, doc)
        self.assertEqual(property_type, "pt_retail")
    '''


if __name__ == '__main__':
    unittest.main()
