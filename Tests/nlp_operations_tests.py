import unittest
import api.natural_search.nlp_operations as ops


class nlp_operations_test(unittest.TestCase):
    
    def test_extract_state(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_state(doc)
        self.assertEqual(states[0].upper(), "VIRGINIA")

        doc = ops.nlp("Show me all the apartments in Richmond, Va.")
        states = ops.extract_state(doc)
        self.assertEqual(states[0].upper(), "VIRGINIA")

    def test_extract_city(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        cities = ops.extract_city(doc)
        self.assertEqual(cities[0].upper(), "RICHMOND")

        doc = ops.nlp("What rental property is in Charleston, SC.")
        cities = ops.extract_city(doc)
        self.assertEqual(cities[0].upper(), "CHARLESTON")

        # Currently Fails
        doc = ops.nlp("What rental property is in New York City")
        cities = ops.extract_city(doc)
        self.assertEqual(cities[0].upper(), "NEW YORK CITY")
   
    def test_extract_zip_code(self):
        doc = ops.nlp("Show me everything in Richmond, Virginia 23221.")
        zip_code = ops.extract_zip_code(doc)
        self.assertEqual(zip_code[0], "23221")

        doc = ops.nlp("List houses in the 23269 area code of Richmond.")
        zip_code = ops.extract_zip_code(doc)
        self.assertEqual(zip_code[0], "23269")

    def test_extract_min_sqft(self):
        doc = ops.nlp("List apartments with at least 1,000 sqft.")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(min_sqft[0], "1,000")

        doc = ops.nlp("Show all 2,000 sqft. apartments")
        min_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(min_sqft[0], "2,000")

    def test_extract_max_sqft(self):
        doc = ops.nlp("List apartments under 3,000 sqft.")
        max_sqft = ops.extract_min_sqft(doc)
        self.assertEqual(max_sqft[0], "3,000")

    def test_extract_min_price(self):
        doc = ops.nlp("Property in Richmond for 250,000$")
        min_price = ops.extract_min_price(doc)
        self.assertEqual(min_price[0], "250,000")

        doc = ops.nlp("List houses in Richmond more than $500,000")
        min_price = ops.extract_min_price(doc)
        self.assertEqual(min_price[0], "500,000")

    def test_extract_max_price(self):
        doc = ops.nlp("Show apartments in Richmond, Virginia less than $1,000 per month.")
        max_price = ops.extract_max_price(doc)
        self.assertEqual(max_price[0], "1,000")

    def test_extract_min_bed(self):
        doc = ops.nlp("List apartments with at least 3 rooms")
        min_bed = ops.extract_min_bed(doc)
        self.assertEqual(min_bed[0], "3")

        doc = ops.nlp("Show all houses with 2 bedrooms")
        min_bed = ops.extract_min_bed(doc)
        self.assertEqual(min_bed[0], "2")

    def test_extract_max_bed(self):
        doc = ops.nlp("apartments in Richmond with less than 17 bedrooms")
        max_bed = ops.extract_max_bed(doc)
        self.assertEqual(max_bed[0], "17")

    def test_extract_pricing_type(self):
        doc = ops.nlp("Show apartments in Richmond, Virginia less than $1,000 per month.")
        pricing_type = ops.extract_pricing_type(doc)
        self.assertEqual(pricing_type[0], "month")

        doc = ops.nlp("List every apartment less than $100,000 per unit?")
        pricing_type = ops.extract_pricing_type(doc)
        self.assertEqual(pricing_type[0], "unit")

if __name__ == '__main__':
    unittest.main()
