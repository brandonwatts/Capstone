import unittest
import smartsearch.tests.all_tests as tests

testSuite = tests.create_test_suite()
runner = unittest.TextTestRunner().run(testSuite)