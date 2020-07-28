import unittest
import meraki
import requests_mock
from .utils import get_mock_response


@requests_mock.Mocker()
class TestRestSession(unittest.TestCase):
    def setUp(self):
        self.api_key = 'FAKE API KEY'
        self.metadata = {'tags': 'test_tag', 'operation': 'test_operation'}
        self.url = '/test'
        self.test_text = 'Test Error'
        self.suppress_logging = True
        self.dashboard = meraki.DashboardAPI(self.api_key, suppress_logging=self.suppress_logging)
        self.mock_response_dict = {"test": "test data"}

    def test_get_500_error(self, mock_request):
        mock_request.get(requests_mock.ANY, status_code=500, text=self.test_text)
        with self.assertRaises(meraki.exceptions.APIError):
            self.dashboard._session.get(self.metadata, self.url)

    def test_get_400_error(self, mock_request):
        mock_request.get(requests_mock.ANY, status_code=400, text=self.test_text)
        with self.assertRaises(meraki.exceptions.APIError):
            self.dashboard._session.get(self.metadata, self.url)

    def test_get_429_error(self, mock_request):
        mock_429_response_headers = {'Retry-After': '0'}
        mock_request.get(requests_mock.ANY, status_code=429, text=self.test_text, headers=mock_429_response_headers)
        with self.assertRaises(meraki.exceptions.APIError):
            self.dashboard._session.get(self.metadata, self.url)
    
    def test_get_other_error(self, mock_request):
        mock_request.get(requests_mock.ANY, status_code=777, text=self.test_text)
        with self.assertRaises(meraki.exceptions.APIError):
            self.dashboard._session.get(self.metadata, self.url)

    def test_get_200_ok(self, mock_request):
        mock_request.get(requests_mock.ANY, status_code=200, json=self.mock_response_dict)
        test_response = self.dashboard._session.get(self.metadata, self.url)
        self.assertEqual(test_response, self.mock_response_dict)


if __name__ == '__main__':
    unittest.main()
