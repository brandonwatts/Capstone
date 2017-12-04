import unittest
import api.natural_search.nlp_operations as ops


class nlp_operations_test(unittest.TestCase):
    
    def test_extract_state(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_state(doc)
        self.assertEqual(states[0], "Virginia")

        doc = ops.nlp("Show me all the apartments in Richmond, Va.")
        states = ops.extract_state(doc)
        self.assertEqual(states[0], "Virginia")
"""
    def test_extract_city(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")

    def test_extract_zip_code(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")

    def test_extract_min_sqft(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")

    def test_extract_max_sqft(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")

    def test_extract_min_price(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")

    def test_extract_max_price(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")

    def test_extract_min_bed(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")

    def test_extract_max_bed(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")
        
    def test_extract_pricing_type(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")
"""
if __name__ == '__main__':
    unittest.main()
