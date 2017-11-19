import unittest
import api.natural_search.nlp_operations as ops


class nlp_operations_test(unittest.TestCase):

    def test_extract_states(self):
        doc = ops.nlp("Show me all the apartments in Richmond, Virginia.")
        states = ops.extract_states(doc)
        self.assertEqual(states[0].text, "Virginia")


if __name__ == '__main__':
    unittest.main()