import unittest
import meraki
import requests_mock

class TestRestSession(unittest.TestCase):
    def setUp(self):
        self.api_key = 'FAKE API KEY'
        self.metadata = {'tags': 'test_tag', 'operation': 'test_operation'}
        with open('tests/mock_responses/test_response.json', 'r') as response:
            self.response_json = response.read()

    def test_get_500_error(self):
        with requests_mock.Mocker() as mock_request:
            dashboard = meraki.DashboardAPI(self.api_key, suppress_logging=True)
            mock_request.get(requests_mock.ANY, status_code=500, text='Test Error')
            with self.assertRaises(meraki.exceptions.APIError):
                dashboard._session.get(self.metadata, '/test')
    def test_get_400_error(self):
        with requests_mock.Mocker() as mock_request:
            dashboard = meraki.DashboardAPI(self.api_key, suppress_logging=True)
            mock_request.get(requests_mock.ANY, status_code=400, text='Test Error')
            with self.assertRaises(meraki.exceptions.APIError):
                dashboard._session.get(self.metadata, '/test')

    def test_get_200_ok(self):
        with requests_mock.Mocker() as mock_request:
            dashboard = meraki.DashboardAPI(self.api_key, suppress_logging=True)
            mock_request.get(requests_mock.ANY, status_code=200, text=self.response_json)
            test = dashboard._session.get(self.metadata, '/test')
            self.assertTrue(test)

if __name__ == '__main__':
    unittest.main()