import unittest
from app import app
import json


class TestRequestTypeGeneral(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def testSimpleNlpResponse(self):
        result = self.app.get('http://localhost:5000/nlp?request=%22Show%20me%20all%20apartments%20in%20Richmond%2C%20Virginia%22&request_type=General')
        data = json.loads(result.data)
        self.assertEqual('Richmond', data.get('city'))
        self.assertEqual('VA', data.get('state'))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
