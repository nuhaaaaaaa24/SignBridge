import unittest
from signbridge import app 

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test 1: Check if homepage loads
    def test_home_status(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # Test 2: Invalid route should return 404
    def test_invalid_route(self):
        response = self.app.get('/invalid')
        self.assertEqual(response.status_code, 404)

    # Test 3: API should handle empty input safely
    def test_empty_input(self):
        response = self.app.post('/predict', json={})
        self.assertIn(response.status_code, [200, 400])

    # Test 4: Security - malformed input
    def test_malformed_input(self):
        response = self.app.post('/predict', data="random_string")
        self.assertIn(response.status_code, [400, 415])

    # Test 5: Check response type
    def test_response_format(self):
        response = self.app.get('/')
        self.assertTrue(response.content_type.startswith('text'))

if __name__ == '__main__':
    unittest.main()
