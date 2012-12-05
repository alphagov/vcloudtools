from __future__ import print_function

import logging
import os
import pprint
import sys

from argh import *
import simplejson

from vcloudtools.api import VCloudAPIClient

log = logging.getLogger(__name__)
parser = ArghParser()


def _dump(obj):
    indent = 2 if os.isatty(sys.stdout.fileno()) else None
    print(simplejson.dumps(obj, namedtuple_as_object=True, indent=indent))


@alias('list')
def lst(args):
    """
    List orgs
    """
    c = VCloudAPIClient()
    for org in c.org_list().orgs:
        _dump(org)


@arg("name")
def show(args):
    """
    Show a specified org
    """
    c = VCloudAPIClient()
    org = c.org(args.name)

    _dump(org)


def main():
    parser.add_commands([lst, show])
    parser.dispatch()


if __name__ == '__main__':
    main()
