import unittest
import meraki
import requests_mock
from .utils import get_mock_response


@requests_mock.Mocker()
class TestNetworks(unittest.TestCase):
    def setUp(self):
        self.api_key = 'FAKE API KEY'
        self.mock_orgid = '2930418'
        self.suppress_logging = True
        self.get_mock_response = get_mock_response
        self.dashboard = meraki.DashboardAPI(self.api_key, suppress_logging=self.suppress_logging)

    def test_getOrganizationNetworks(self, mock_request):
        mock_response_json = self.get_mock_response('getOrganizationNetworks.json')
        url = f'{self.dashboard._session._base_url}/organizations/{self.mock_orgid}/networks'
        mock_request.get(url, text=mock_response_json)
        my_nets = self.dashboard.networks.getOrganizationNetworks(self.mock_orgid)
        self.assertTrue('organizationId' in my_nets[0].keys())


if __name__ == '__main__':
    unittest.main()
