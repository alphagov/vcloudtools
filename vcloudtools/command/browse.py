from __future__ import print_function

import logging
import sys

from argh import *
from vcloudtools.api import VCloudAPIClient

log = logging.getLogger(__name__)
parser = ArghParser()

@arg('path', help='Path to fetch', default='/')
def browse(args):
    """
    Browse the vCloud API using the built-in hypermedia links
    """
    c = VCloudAPIClient()
    res = c.browse(args.path)

    print('HTTP/1.1 {0} {1}'.format(res.status_code, res.reason))

    for k, v in res.headers.items():
        print("{0}: {1}".format(k, v))

    print()
    print(res.content)

def main():
    dispatch_command(browse)

if __name__ == '__main__':
    main()
