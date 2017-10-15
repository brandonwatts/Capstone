import unittest
from nlp_api import parse_entities,parse_syntax


class NlpApiTestCase(unittest.TestCase):
    """Tests for `nlp_api.py`."""

    def test_parsing_entities(self):
        entities = parse_entities("George Washington was the first president of the United States.")
        self.assertEqual(entities[0].name, "George Washington")
        self.assertEqual(entities[1].name, "United States")

    def test_parsing_syntax(self):
        syntax = parse_syntax("George Washington was the first president of the United States.")
        self.assertEqual(syntax[0].text.content, "George")
        self.assertEqual(syntax[0].part_of_speech.tag, 6)

if __name__ == '__main__':
    unittest.main()