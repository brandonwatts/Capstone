import unittest
import app

class TestEndpointRequestToNlpTransfer(unittest.TestCase):

    # Need a way to test when an invalid text is passed to the nlp.  But maybe not if we assume happy path?
    def testValidQuery(self):
        request = "Show me all apartments in Richmond, Virginia"
        nlp_result = app.nlp.parse(request)

class TestNlpToApartmentsResponseTransfer(unittest.TestCase):

    def testSimpleNlpResponse(self):
        request = "Show me all apartments in Richmond, Virginia"
        nlp_result = app.nlp.parse(request)
        apartment_api = app.ApartmentsAPI(nlp_result)
        self.assertEqual(nlp_result['city'], apartment_api.nlp_response['city'])
        self.assertEqual(nlp_result['state'], apartment_api.nlp_response['state'])

    def testComplexNlpResponse(self):
        request = "Show me all the 3 bedroom apartments that have a pool and are cat friendly in Richmond, Virginia"
        nlp_result = app.nlp.parse(request)
        apartment_api = app.ApartmentsAPI(nlp_result)
        self.assertEqual(nlp_result['city'], apartment_api.nlp_response['city'])
        self.assertEqual(nlp_result['cat_friendly'], apartment_api.nlp_response['cat_friendly'])
        self.assertEqual(nlp_result['has_pool'], apartment_api.nlp_response['has_pool'])

if __name__ == '__main__':
    unittest.main()