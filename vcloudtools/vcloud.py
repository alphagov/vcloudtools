from collections import namedtuple

_Link = namedtuple('Link', 'type href rel name')
class Link(_Link):
    def __new__(cls, type, href, rel, name=None):
        return super(cls, Link).__new__(cls, type, href, rel, name)

_Org = namedtuple('Org', 'type href name id full_name description links')
class Org(_Org):
    def __new__(cls, type, href, name, id=None, full_name=None, description=None, links=None):
        return super(cls, Org).__new__(cls, type, href, name, id, full_name, description, links)


_OrgList = namedtuple('OrgList', 'orgs')
class OrgList(_OrgList):

    def org_by_name(self, name):
        for o in self.orgs:
            if o.name == name:
                return o
        return None
