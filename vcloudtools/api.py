from collections import defaultdict
from datetime import datetime
from os import environ as env
import json
import logging

import lxml.etree
import requests

from vcloudtools.vcloud import Link, OrgList, Org

log = logging.getLogger(__name__)


VCLOUD_AUTH_HEADER = 'x-vcloud-authorization'
VCLOUD_VERSION = '1.5'
VCLOUD_MIME = 'application/*+xml;version=%s' % VCLOUD_VERSION
VCLOUD_NS = {
    'vcloud': 'http://www.vmware.com/vcloud/v%s' % VCLOUD_VERSION
}


class ClientError(Exception):
    pass


class APIError(Exception):
    pass


class VCloudAPIClient(object):
    def __init__(self, root=None):
        """
        Create a new instance of the vCloud API client, optionally specifying the API root URL
        """

        self._session = requests.Session(headers={'accept': VCLOUD_MIME})
        self.token = envget('auth_token')

        if root is not None:
            self.root = root
        elif envget('api_root') is not None:
            self.root = envget('api_root')
        else:
            msg = "No known API root for vCloud. Perhaps you need to set ${0}?".format(envkey('api_root'))
            raise ClientError(msg)

        self._links = None

        if self.logged_in:
            self._links = self._fetch_initial_links()

        log.debug("Created %s", self)

    def _req(self, method, url, _raise=True, *args, **kwargs):
        """
        Make and error check a request in the current session
        """
        res = self._session.request(method, url, *args, **kwargs)
        if _raise:
            _custom_raise_for_status(res)
        return res

    def _url(self, path):
        """
        Return an absolute URL for the specified path
        """
        return self.root + path

    def _lookup(self, typ):
        """
        Look up a URL for a resource of the specified type
        """
        full_typ = 'application/vnd.vmware.{0}+xml'.format(typ)

        if full_typ in self._links:
            return self._links[full_typ][0].href
        else:
            raise APIError("Don't know anything about type '{0}'".format(typ))

    def _fetch_initial_links(self):
        """
        Fetch the "root" resource URLs for this session
        """
        res = self._req('get', self._url('/session'))

        etree = lxml.etree.fromstring(res.content)
        links = _parse_links(etree)

        return links

    def login(self, username, password):
        """
        Retrieve an auth token from the vCloud API using a username and password
        """
        res = self._req(
            'post',
            self._url('/sessions'),
            auth=(username, password),
        )

        self.token = res.headers[VCLOUD_AUTH_HEADER]

    def browse(self, path='/'):
        """
        Make an arbitrary request to the vCloud API at the specified path
        """
        res = self._req('get', self._url(path))
        return res

    def org_list(self):
        """
        Retrieve the OrgList
        """
        res = self._req('get', self._lookup('vcloud.orgList'))

        etree = lxml.etree.fromstring(res.content)
        return _parse_org_list(etree)

    def org(self, name):
        """
        Retrieve an org by name
        """
        org_short = self.org_list().org_by_name(name)

        res = self._req('get', org_short.href)

        etree = lxml.etree.fromstring(res.content)
        return _parse_org(etree)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, tok):
        self._token = tok
        self._session.headers[VCLOUD_AUTH_HEADER] = self._token

    @property
    def logged_in(self):
        """
        Return a boolean representing logged-in status
        """
        res = self._req('get', self._url('/session'), _raise=False)
        return res.ok

    def __str__(self):
        return '<VCloudAPIClient {0}>'.format(self.root)



def envkey(key):
    return 'VCLOUD_{0}'.format(key.upper())


def envget(key, default=None):
    return env.get(
        envkey(key),
        default
    )


def _parse_links(el):
    res = defaultdict(list)
    for c in el.findall('vcloud:Link', VCLOUD_NS):
        link = _parse_link(c)
        res[link.type].append(link)
    return res


def _parse_link(el):
    return Link(**el.attrib)


def _parse_org_list(el):
    orgs = [_parse_org_short(c) for c in el.findall('vcloud:Org', VCLOUD_NS)]
    return OrgList(orgs=orgs)


def _parse_org_short(el):
    return Org(**el.attrib)


def _parse_org(el):
    type_ = el.attrib['type']
    href  = el.attrib['href']
    name  = el.attrib['name']
    id_   = el.attrib['id']

    full_name = el.find('vcloud:FullName', VCLOUD_NS).text
    description = el.find('vcloud:Description', VCLOUD_NS).text

    links = _parse_links(el)

    return Org(
        type=type_,
        href=href,
        name=name,
        id=id_,
        full_name=full_name,
        description=description,
        links=links
    )


def _custom_raise_for_status(res):
    try:
        res.raise_for_status()
    except requests.RequestException as err:
        raise APIError(err)


