import unittest
import meraki
import requests_mock
from .utils import get_mock_response


@requests_mock.Mocker()
class TestRestSession(unittest.TestCase):
    def setUp(self):
        self.mock_api_key = 'FAKE API KEY'
        self.mock_metadata = {'tags': 'test_tag', 'operation': 'test_operation'}
        self.mock_url = '/test'
        self.mock_response_text = 'Test Error'
        self.suppress_logging = True
        self.dashboard = meraki.DashboardAPI(self.mock_api_key, suppress_logging=self.suppress_logging)
        self.mock_response_json = {"test": "test data"}
        self.mock_request_json = {"test": "test data"}

    def test_get_500_error(self, mock_request):
        mock_request.get(requests_mock.ANY, status_code=500, text=self.mock_response_text)
        with self.assertRaises(meraki.exceptions.APIError):
            self.dashboard._session.get(self.mock_metadata, self.mock_url)

    def test_get_400_error(self, mock_request):
        mock_request.get(requests_mock.ANY, status_code=400, text=self.mock_response_text)
        with self.assertRaises(meraki.exceptions.APIError):
            self.dashboard._session.get(self.mock_metadata, self.mock_url)

    def test_get_429_error(self, mock_request):
        mock_429_response_headers = {'Retry-After': '0'}
        mock_request.get(requests_mock.ANY, status_code=429, text=self.mock_response_text, headers=mock_429_response_headers)
        with self.assertRaises(meraki.exceptions.APIError):
            self.dashboard._session.get(self.mock_metadata, self.mock_url)

    def test_get_302_error(self, mock_request):
        mock_302_response_headers = {'Location': 'meraki.com/api/v'}
        mock_request.get(requests_mock.ANY, status_code=302, text=self.mock_response_text, headers=mock_302_response_headers)
        with self.assertRaises(meraki.exceptions.APIError):
            self.dashboard._session.get(self.mock_metadata, self.mock_url)
    
    def test_get_other_error(self, mock_request):
        mock_request.get(requests_mock.ANY, status_code=777, text=self.mock_response_text)
        with self.assertRaises(meraki.exceptions.APIError):
            self.dashboard._session.get(self.mock_metadata, self.mock_url)

    def test_get_200_ok(self, mock_request):
        mock_request.get(requests_mock.ANY, status_code=200, json=self.mock_response_json)
        test_response = self.dashboard._session.get(self.mock_metadata, self.mock_url)
        self.assertEqual(test_response, self.mock_response_json)

    def test_post_200_ok(self, mock_request):
        mock_request.post(requests_mock.ANY, status_code=200, json=self.mock_response_json)
        test_response = self.dashboard._session.post(self.mock_metadata, self.mock_url, json=self.mock_request_json)
        self.assertEqual(test_response, self.mock_response_json)

    def test_put_200_ok(self, mock_request):
        mock_request.put(requests_mock.ANY, status_code=200, json=self.mock_response_json)
        test_response = self.dashboard._session.put(self.mock_metadata, self.mock_url, json=self.mock_request_json)
        self.assertEqual(test_response, self.mock_response_json)

    def test_delete_200_ok(self, mock_request):
        mock_request.delete(requests_mock.ANY, status_code=200, json=self.mock_response_json)
        test_response = self.dashboard._session.delete(self.mock_metadata, self.mock_url)
        self.assertEqual(test_response, None)


if __name__ == '__main__':
    unittest.main()
