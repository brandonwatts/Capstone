import unittest
import Api.NLP as ops


class nlp_operations_test(unittest.TestCase):
    
    def test_extract_state(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_state(doc)
        self.assertEqual(len(states), 1)
        self.assertEqual(states[0].upper(), "VIRGINIA")

        doc = ops.nlp("Show me all the apartments in Richmond, Va.")
        states = ops.extract_state(doc)
        self.assertEqual(len(states), 1)
        self.assertEqual(states[0].upper(), "VIRGINIA")

        # Two word state with comma.
        doc = ops.nlp("What are all the 3 bedrooms in Providence, Rhode Island")
        states = ops.extract_state(doc)
        self.assertEqual(len(states), 2)
        self.assertEqual(states[0].upper(), "RHODE")
        self.assertEqual(states[1].upper(), "ISLAND")

        # Two word state without comma.
        doc = ops.nlp("Show me all the 3 bedrooms in New York City New York")
        cities = ops.extract_state(doc)
        self.assertEqual(len(cities), 2)
        self.assertEqual(cities[0].upper(), "NEW")
        self.assertEqual(cities[1].upper(), "YORK")

    def test_extract_city(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        cities = ops.extract_city(doc)
        self.assertEqual(cities[0].upper(), "RICHMOND")

        doc = ops.nlp("What rental property is in Charleston, SC.")
        cities = ops.extract_city(doc)
        self.assertEqual(cities[0].upper(), "CHARLESTON")

        # Similiar city name to state name with comma.
        doc = ops.nlp("Show me all the 3 bedrooms in New York City, New York")
        cities = ops.extract_city(doc)
        self.assertEqual(len(cities), 3)
        self.assertEqual(cities[0].upper(), "NEW")
        self.assertEqual(cities[1].upper(), "YORK")
        self.assertEqual(cities[2].upper(), "CITY")

        # Similiar city name to state name without comma.
        doc = ops.nlp("Show me all the 3 bedrooms in New York City New York")
        cities = ops.extract_city(doc)
        self.assertEqual(len(cities), 3)
        self.assertEqual(cities[0].upper(), "NEW")
        self.assertEqual(cities[1].upper(), "YORK")
        self.assertEqual(cities[2].upper(), "CITY")
   
    def test_extract_zip_code(self):
        doc = ops.nlp("Show me everything in Richmond, Virginia 23221.")
        zip_code = ops.extract_zip_code(doc)
        self.assertEqual(len(zip_code), 1)
        self.assertEqual(zip_code[0], "23221")

        doc = ops.nlp("List houses in the 23269 area code of Richmond.")
        zip_code = ops.extract_zip_code(doc)
        self.assertEqual(len(zip_code), 1)
        self.assertEqual(zip_code[0], "23269")

    def test_extract_min_sqft(self):
        doc = ops.nlp("Show all 2,000 feet apartments")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(len(min_sqft), 1)
        self.assertEqual(min_sqft[0], "2,000")

        doc = ops.nlp("Show all apartments that are greater than 2,000 squarefeet in Richmond")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(len(min_sqft), 1)
        self.assertEqual(min_sqft[0], "2,000")

        doc = ops.nlp("Show all apartments that are greater than 2,000 squarefoot in Richmond")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(len(min_sqft), 1)
        self.assertEqual(min_sqft[0], "2,000")

        doc = ops.nlp("Show all apartments that are greater than 2,000 sqft in Richmond")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(len(min_sqft), 1)
        self.assertEqual(min_sqft[0], "2,000")

        doc = ops.nlp("List apartments with at greater than 1,000 sqft.")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(len(min_sqft), 1)
        self.assertEqual(min_sqft[0], "1,000")

        doc = ops.nlp("List apartments with at greater than 1,000 sq")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(len(min_sqft), 1)
        self.assertEqual(min_sqft[0], "1,000")

        doc = ops.nlp("List apartments with at greater than 1,000 ft")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(len(min_sqft), 1)
        self.assertEqual(min_sqft[0], "1,000")

        doc = ops.nlp("Show me all apartments that are at least 50,000 sqft and under 60,000 sqft")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(len(min_sqft), 1)
        self.assertEqual(min_sqft[0], "50,000")

    def test_extract_max_sqft(self):
        # Fail
        doc = ops.nlp("Show me all apartments that are under 60,000 sqft")
        max_sqft = ops.extract_max_sqft(doc)
        self.assertEqual(len(max_sqft), 1)
        self.assertEqual(max_sqft[0], "60,000")

        doc = ops.nlp("Show me all apartments that are at least 50,000 sqft and under 60,000 sqft")
        max_sqft = ops.extract_max_sqft(doc)
        self.assertEqual(len(max_sqft), 1)
        self.assertEqual(max_sqft[0], "60,000")

    def test_extract_min_price(self):
        doc = ops.nlp("Property in Richmond for 250,000$")
        min_price = ops.extract_min_price(doc)
        self.assertEqual(len(min_price), 1)
        self.assertEqual(min_price[0], "250,000")

        doc = ops.nlp("List houses in Richmond more than $500,000")
        min_price = ops.extract_min_price(doc)
        self.assertEqual(len(min_price), 1)
        self.assertEqual(min_price[0], "500,000")

        doc = ops.nlp("List houses in Richmond that are greater than $500,000")
        min_price = ops.extract_min_price(doc)
        self.assertEqual(len(min_price), 1)
        self.assertEqual(min_price[0], "500,000")

        doc = ops.nlp("List houses in Richmond that are over $500,000")
        min_price = ops.extract_min_price(doc)
        self.assertEqual(len(min_price), 1)
        self.assertEqual(min_price[0], "500,000")

    def test_extract_max_price(self):
        doc = ops.nlp("Show apartments in Richmond, Virginia less than $1,000 per month.")
        max_price = ops.extract_max_price(doc)
        self.assertEqual(len(max_price), 1)
        self.assertEqual(max_price[0], "1,000")

        # Fail
        doc = ops.nlp("I want all apartments in Chicago that are under $1,000 per month.")
        max_price = ops.extract_max_price(doc)
        self.assertEqual(len(max_price), 1)
        self.assertEqual(max_price[0], "1,000")

        doc = ops.nlp("I want all apartments in Chicago that are below $1,000 per month.")
        max_price = ops.extract_max_price(doc)
        self.assertEqual(len(max_price), 1)
        self.assertEqual(max_price[0], "1,000")

    def test_extract_min_bed(self):
        doc = ops.nlp("List apartments with at least 3 rooms")
        min_bed = ops.extract_min_bed(doc)
        self.assertEqual(len(min_bed), 1)
        self.assertEqual(min_bed[0], "3")

        doc = ops.nlp("Show all houses with 2 bedrooms")
        min_bed = ops.extract_min_bed(doc)
        self.assertEqual(len(min_bed), 1)
        self.assertEqual(min_bed[0], "2")

    def test_extract_max_bed(self):
        doc = ops.nlp("Apartments in Richmond with less than 17 bedrooms")
        max_bed = ops.extract_max_bed(doc)
        self.assertEqual(len(max_bed), 1)
        self.assertEqual(max_bed[0], "17")

        # Fail
        doc = ops.nlp("Apartments in Richmond that have under 17 bedrooms")
        max_bed = ops.extract_max_bed(doc)
        self.assertEqual(len(max_bed), 1)
        self.assertEqual(max_bed[0], "17")

    def test_extract_pricing_type(self):
        doc = ops.nlp("Show apartments in Richmond, Virginia less than $1,000 per month.")
        pricing_type = ops.extract_pricing_type(doc)
        self.assertEqual(len(pricing_type), 1)
        self.assertEqual(pricing_type[0], "month")

        doc = ops.nlp("List every apartment less than $100,000 per unit?")
        self.assertEqual(len(pricing_type), 1)
        pricing_type = ops.extract_pricing_type(doc)
        self.assertEqual(pricing_type[0], "unit")

    def test_extract_address(self):
        # Fails.  Picks up West Avenue but not the 1300 part.
        doc = ops.nlp("Give me all the apartments near 1300 West Avenue, Richmond, Virginia")
        address = ops.extract_address(doc)
        self.assertEqual(len(address), 3)
        self.assertEqual(address[0], "1300")
        self.assertEqual(address[1], "West")
        self.assertEqual(address[2], "Avenue")

        doc = ops.nlp("Give me all the apartments near 1700 West Highway in Virginia")
        address = ops.extract_address(doc)
        self.assertEqual(len(address), 3)
        self.assertEqual(address[0], "1700")
        self.assertEqual(address[1], "West")
        self.assertEqual(address[2], "Highway")

        doc = ops.nlp("Give me all the apartments within 3 miles of 555 Jefferson Road in Virginia")
        address = ops.extract_address(doc)
        self.assertEqual(len(address), 3)
        self.assertEqual(address[0], "555")
        self.assertEqual(address[1], "Jefferson")
        self.assertEqual(address[2], "Road")

    def test_extract_build_year(self):
        doc = ops.nlp("Give me all buildings built since 1990")
        build_year = ops.extract_build_year(doc)
        self.assertEqual(len(build_year), 1)
        self.assertEqual(build_year[0], "1990")

        doc = ops.nlp("Give me all buildings built between 1990 and 2005")
        build_year = ops.extract_build_year(doc)
        print(len(build_year))
        self.assertEqual(len(build_year), 2)
        self.assertEqual(build_year[0], "1990")
        self.assertEqual(build_year[1], "2005")

    def test_extract_dog_friendly(self):
        doc = ops.nlp("Show me all apartments in Richmond, Virginia that are dog friendly")
        dog_friendly = ops.extract_dog_friendly(doc)
        self.assertEqual(dog_friendly, True)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that are not dog friendly")
        dog_friendly = ops.extract_dog_friendly(doc)
        self.assertEqual(dog_friendly, False)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that love dogs")
        dog_friendly = ops.extract_dog_friendly(doc)
        self.assertEqual(dog_friendly, True)

    def test_extract_dog_friendly(self):
        doc = ops.nlp("Show me all apartments in Richmond, Virginia that are cat friendly")
        cat_friendly = ops.extract_cat_friendly(doc)
        self.assertEqual(cat_friendly, True)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that are not cat friendly")
        cat_friendly = ops.extract_cat_friendly(doc)
        self.assertEqual(cat_friendly, False)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that love cats")
        cat_friendly = ops.extract_cat_friendly(doc)
        self.assertEqual(cat_friendly, True)

    def test_has_pool(self):
        doc = ops.nlp("Show me all apartments in Richmond, Virginia that have a pool")
        has_pool = ops.extract_has_pool(doc)
        self.assertEqual(has_pool, True)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that do not have a pool")
        has_pool = ops.extract_has_pool(doc)
        self.assertEqual(has_pool, False)

    def test_has_elevator(self):
        doc = ops.nlp("Show me all buildings in Richmond, Virginia that have an elevator")
        has_elevator = ops.extract_has_elevator(doc)
        self.assertEqual(has_elevator, True)

        doc = ops.nlp("Show me all buildings in Richmond, Virginia that do not have an elevator")
        has_elevator = ops.extract_has_elevator(doc)
        self.assertEqual(has_elevator, False)

        doc = ops.nlp("Show me all buildings in Richmond, Virginia that have a lift")
        has_elevator = ops.extract_has_elevator(doc)
        self.assertEqual(has_elevator, True)

    def test_has_fitness_center(self):
        doc = ops.nlp("Show me all buildings in Richmond, Virginia that have a fitness center nearby")
        has_fitness_center = ops.extract_has_fitness_center(doc)
        self.assertEqual(has_fitness_center, True)

        doc = ops.nlp("Show me all buildings in Richmond, Virginia that do not have a fitness center nearby")
        has_fitness_center = ops.extract_has_fitness_center(doc)
        self.assertEqual(has_fitness_center, False)

        doc = ops.nlp("Show me all buildings in Richmond, Virginia have a local gym")
        has_fitness_center = ops.extract_has_fitness_center(doc)
        self.assertEqual(has_fitness_center, False)

    def test_has_wheelchair_access(self):
        doc = ops.nlp("Show me all buildings in Richmond, Virginia that have a wheelchair access")
        has_wheelchair_access = ops.extract_has_wheelchair_access(doc)
        self.assertEqual(has_wheelchair_access, True)

        doc = ops.nlp("Show me all buildings in Richmond, Virginia that do not have a wheelchair access")
        has_wheelchair_access = ops.extract_has_wheelchair_access(doc)
        self.assertEqual(has_wheelchair_access, False)

        doc = ops.nlp("Show me all buildings in Richmond, Virginia that have handicap access")
        has_wheelchair_access = ops.extract_has_wheelchair_access(doc)
        self.assertEqual(has_wheelchair_access, True)

    def test_has_dishwasher(self):
        doc = ops.nlp("Show me all apartments in Richmond, Virginia that have a dishwasher")
        has_dishwasher_access = ops.extract_has_dishwasher(doc)
        self.assertEqual(has_dishwasher_access, True)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that do not have a dishwasher")
        has_dishwasher_access = ops.extract_has_dishwasher(doc)
        self.assertEqual(has_dishwasher_access, False)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that have a dish cleaner")
        has_dishwasher_access = ops.extract_has_dishwasher(doc)
        self.assertEqual(has_dishwasher_access, True)

    def test_has_air_conditioning(self):
        doc = ops.nlp("Show me all apartments in Richmond, Virginia that have air conditioning")
        has_air_conditioning = ops.extract_has_air_conditioning(doc)
        self.assertEqual(has_air_conditioning, True)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that does not have air conditioning")
        has_air_conditioning = ops.extract_has_air_conditioning(doc)
        self.assertEqual(has_air_conditioning, False)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that have heating and cooling")
        has_air_conditioning = ops.extract_has_air_conditioning(doc)
        self.assertEqual(has_air_conditioning, True)

    def test_parking(self):
        doc = ops.nlp("Show me all apartments in Richmond, Virginia that have parking")
        has_parking = ops.extract_has_parking(doc)
        self.assertEqual(has_parking, True)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that do not have parking")
        has_parking = ops.extract_has_parking(doc)
        self.assertEqual(has_parking, False)

        doc = ops.nlp("Show me all houses in Richmond, Virginia that have a parking garage")
        has_parking = ops.extract_has_parking(doc)
        self.assertEqual(has_parking, True)

    def test_furnished(self):
        doc = ops.nlp("Show me all apartments in Richmond, Virginia that are furnished")
        is_furnished = ops.extract_is_furnished(doc)
        self.assertEqual(is_furnished, True)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that are not furnished")
        is_furnished = ops.extract_is_furnished(doc)
        self.assertEqual(is_furnished, False)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that already have furniture")
        is_furnished = ops.extract_is_furnished(doc)
        self.assertEqual(is_furnished, True)

    def test_laundry_facilities(self):
        doc = ops.nlp("Show me all apartments in Richmond, Virginia that have laundry facilities")
        has_laundry_facilities = ops.extract_has_laundry_facilities(doc)
        self.assertEqual(has_laundry_facilities, True)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that do not have laundry facilities")
        has_laundry_facilities = ops.extract_has_laundry_facilities(doc)
        self.assertEqual(has_laundry_facilities, False)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that have a washing machine")
        has_laundry_facilities = ops.extract_has_laundry_facilities(doc)
        self.assertEqual(has_laundry_facilities, True)

        doc = ops.nlp("Show me all apartments in Richmond, Virginia that have a washer and dryer")
        has_laundry_facilities = ops.extract_has_laundry_facilities(doc)
        self.assertEqual(has_laundry_facilities, True)

    def test_property_type(self):
        doc = ops.nlp("Show me all industrial buildings in Richmond, Virginia")
        property_type = ops.extract_property_type(doc)
        self.assertEqual(len(property_type), 1)
        self.assertEqual(property_type[0], "pt_industrial")

        doc = ops.nlp("Show me all non-retail buildings in Richmond, Virginia")
        property_type = ops.extract_property_type(doc)
        self.assertEqual(len(property_type), 1)
        self.assertEqual(property_type[0], "pt_retail")

if __name__ == '__main__':
    unittest.main()
