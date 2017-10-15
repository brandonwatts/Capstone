import unittest

from api.natural_search.speech_api import parse_speech


class SpeechApiTestCase(unittest.TestCase):
    """Tests for `nlp_api.py`."""

    def test_parse_speech(self):
        speech = parse_speech("../../Test Speech Files/houses_in_richmond_3_bdrm.wav")
        self.assertEqual(speech.results[0].alternatives[0].transcript,"show me all the houses in Richmond with 3 bedrooms")

if __name__ == '__main__':
    unittest.main()