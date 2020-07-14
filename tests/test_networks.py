import unittest
import meraki
import requests_mock

class TestNetworks(unittest.TestCase):
    def setUp(self):
        self.api_key = 'FAKE API KEY'

    def test_getOrganizationNetworks(self):
        with open('tests/mock_responses/getOrganizationNetworks.json', 'r') as response:
            response_json = response.read()
        with requests_mock.Mocker() as mock_request:
            organizationId = '2930418'
            dashboard = meraki.DashboardAPI(self.api_key, suppress_logging=True)
            mock_request.get(f'{dashboard._session._base_url}/organizations/{organizationId}/networks', text=response_json)
            my_nets = dashboard.networks.getOrganizationNetworks(organizationId)
            self.assertTrue('organizationId' in my_nets[0].keys())

if __name__ == '__main__':
    unittest.main()