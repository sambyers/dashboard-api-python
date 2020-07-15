import unittest
import meraki
import requests_mock
from .utils import get_mock_response


@requests_mock.Mocker()
class TestOrganizations(unittest.TestCase):
    def setUp(self):
        self.api_key = 'FAKE API KEY'
        self.mock_orgid = '2930418'
        self.suppress_logging = True
        self.get_mock_response = get_mock_response
        self.dashboard = meraki.DashboardAPI(self.api_key, suppress_logging=self.suppress_logging)

    def test_getOrganizations(self, mock_request):
        mock_response_json = self.get_mock_response('getOrganizations.json')
        url = f'{self.dashboard._session._base_url}/organizations'
        mock_request.get(url, text=mock_response_json)
        my_orgs = self.dashboard.organizations.getOrganizations()
        self.assertTrue('id' in my_orgs[0].keys())

    def test_getOrganization(self, mock_request):
        mock_response_json = self.get_mock_response('getOrganization.json')
        url = f'{self.dashboard._session._base_url}/organizations/{self.mock_orgid}'
        mock_request.get(url, text=mock_response_json)
        my_org = self.dashboard.organizations.getOrganization(self.mock_orgid)
        self.assertTrue('id' in my_org.keys())


if __name__ == '__main__':
    unittest.main()
