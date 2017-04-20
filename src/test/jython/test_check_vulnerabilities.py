import requests_mock

from responses import GET_APPLICATION_RESPONSE, GET_PROJECT_RESPONSE, GET_TASKS_RESPONSE
from sdelements.SDEClient import SDEClient


@requests_mock.Mocker()
class TestCheckVulnerabilities(object):

    def test_check_vulnerabilities_ok(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_TASKS_URI % (sde_client.url, '1'), json=GET_TASKS_RESPONSE)
        m.register_uri('GET', SDEClient.GET_PROJECTS % (sde_client.url, '1', 'Project Test'), json=GET_PROJECT_RESPONSE)
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'Application Test'), json=GET_APPLICATION_RESPONSE)
        result = sde_client.check_vulnerabilities('Application Test', 'Project Test', 100,0,0)
        assert result['highResult'] == 100
        assert result['mediumResult'] == 0
        assert result['lowResult'] == 0
        assert result['success'] == True

    def test_check_vulnerabilities_failed(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_TASKS_URI % (sde_client.url, '1'), json=GET_TASKS_RESPONSE)
        m.register_uri('GET', SDEClient.GET_PROJECTS % (sde_client.url, '1', 'Project Test'), json=GET_PROJECT_RESPONSE)
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'Application Test'), json=GET_APPLICATION_RESPONSE)
        result = sde_client.check_vulnerabilities('Application Test', 'Project Test', 50,0,0)
        assert result['highResult'] == 100
        assert result['mediumResult'] == 0
        assert result['lowResult'] == 0
        assert result['success'] == False