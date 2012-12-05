from __future__ import print_function

from getpass import getpass, _raw_input
import logging
import sys

from argh import *
from vcloudtools.api import VCloudAPIClient, envkey

log = logging.getLogger(__name__)
parser = ArghParser()

def login_if_needed(vcloud):
    if vcloud.logged_in:
        log.info("Already logged in")
        return

    print("Please log into vCloud", file=sys.stderr)
    username = _raw_input("Username: ")
    password = getpass("Password: ")

    vcloud.login(username, password)

def login(args):
    """
    Log into a vCloud instance, and print the resulting auth token.
    """
    c = VCloudAPIClient()

    login_if_needed(c)

    print("export {0}='{1}'".format(envkey('auth_token'), c.token))

def main():
    dispatch_command(login)

if __name__ == '__main__':
    main()
