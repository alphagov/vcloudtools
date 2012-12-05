import copy
from nose.tools import *

from vcloudtools.vcloud import Link, Org, OrgList

MOCK_LINK = {
    'type': 'application/foo+xml',
    'href': 'https://test/foo',
    'rel': 'test_rel',
    'name': 'foo',
}

MOCK_ORG = {
    'type': 'application/vnd.vmware.vcloud.org+xml',
    'href': 'http://test-api-client/org/734772e4-166f-4dcc-9391-d35ddafce90e',
    'name': 'Test-Org',
    'id': 'urn:vcloud:org:734772e4-166f-4dcc-9391-d35ddafce90e',
    'full_name': 'Test Organisation',
    'description': None,
    'links': { },
}

class TestLink(object):

    def setup(self):
        self.l = copy.deepcopy(MOCK_LINK)

    def test_name_optional(self):
        self.l.pop('name')
        link = Link(**self.l)
        assert_equal(link.name, None)

class TestOrg(object):

    def test_optional(self):
        def _test(key):
            o = copy.deepcopy(MOCK_ORG)
            o.pop(key)
            org = Org(**o)
            assert_equal(getattr(org, key), None)

        for k in ['id', 'full_name', 'description', 'links']:
            yield _test, k

class TestOrgList(object):

    def test_org_by_name(self):
        foo = Org(type='testtype', href='testhref', name='foo')
        bar = Org(type='testtype', href='testhref', name='bar')
        baz = Org(type='testtype', href='testhref', name='baz')

        olist = OrgList(orgs=[foo, bar, baz])

        assert_equal(olist.org_by_name('bar'), bar)
