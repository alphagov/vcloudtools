import logging

from ..helpers import *

from vcloudtools.api import VCloudAPIClient, envkey, envget

# This environment variable is expected to be set when testing. Tox will set
# it (see tox.ini)
API_ROOT = os.environ.get('VCLOUD_API_ROOT')

class TestVCloudAPIClient(RequestMockTestCase):

    def setup(self):
        self.session_to_patch = 'vcloudtools.api.requests.Session'
        super(TestVCloudAPIClient, self).setup()

        self.login()

    def login(self):
        session_xml = fixture('session')
        self.register_response('post', API_ROOT + '/sessions', 200, {'x-vcloud-authorization': 'test_token'}, session_xml)
        self.register_response('get', API_ROOT + '/session', 200, {}, session_xml)

    def logout(self):
        self.register_response('get', API_ROOT + '/session', 401)

    def test_login_should_set_token(self):
        c = VCloudAPIClient()
        assert_equal(c.token, None)
        c.login('foo', 'bar')
        assert_equal(c.token, 'test_token')

    def test_browse_gets_api_root_with_no_args(self):
        c = VCloudAPIClient()
        self.register_response('get', API_ROOT + '/', 200, content='FOO BAR')

        res = c.browse()
        assert_equal(res.content, 'FOO BAR')

    def test_browse_gets_specified_path(self):
        c = VCloudAPIClient()
        self.register_response('get', API_ROOT + '/wibble', 200, content='BAZ BAT')

        res = c.browse('/wibble')
        assert_equal(res.content, 'BAZ BAT')

    def test_org_list_should_return_list_of_orgs(self):
        c = VCloudAPIClient()
        org_list_xml = fixture('orglist')

        # org_list should work out where to look from the hypermedia returned
        # at the /session path. "/myCustomOrgListPath/" is where the orgList
        # is defined to exist in the "session" fixture
        self.register_response('get', API_ROOT + '/myCustomOrgListPath/', 200, {}, org_list_xml)

        org_list = c.org_list()
        assert_equal(len(org_list.orgs), 3)


def test_envkey():
    assert_equal(envkey('foo'), 'VCLOUD_FOO')
    assert_equal(envkey('foo_bar'), 'VCLOUD_FOO_BAR')


@patch('vcloudtools.api.env')
def test_envget(env_mock):
    env_mock.get.return_value = 'fooval'
    assert_equal(envget('foo'), 'fooval')
