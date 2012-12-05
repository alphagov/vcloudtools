vcloudtools
===========

A set of commandline utilities to aid working with the VMWare vCloud API. 

At the moment, ``vcloudtools`` is pretty minimal, but there's still enough
here to be useful. In addition to a Python API client
(``vcloudtools.api.VCloudAPIClient``), there's a series of small command line
utilities to help interact with vCloud Director's HTTP API.

Installation
------------

``vcloudtools`` is available on the `Python Package Index
<http://pypi.python.org/pypi/vcloudtools>`_::

    $ pip install vcloudtools

Usage
-----

First, tell ``vcloudtools`` where your vCloud Director API is by adding an
environment variable to your ``.bash_profile`` or similar::

    $ echo "export VCLOUD_API_ROOT=https://vcd.example.com/api" >> ~/.bash_profile
    $ exec $SHELL

Then, login to the VCD API::

    $ eval `vcloud-login`

You can now use ``vcloudtools`` without further authentication hassles. So
far, the available tools include ``vcloud-org``::

    $ vcloud-org list
    $ vcloud-org show My-Org-Name

``vcloud-org`` will emit JSON, which you can parse with `jsontool
<https://npmjs.org/package/jsontool>`_ or similar.

You can also manually browse the API with ``vcloud-browse``::

    $ vcloud-browse /session
    $ vcloud-browse /org/7318a9a7-cc79-4f88-b8f8-ddddec6873f8

Hacking
-------

Please make sure you run the tests with::

    $ pip install tox
    $ tox

License
-------

``vcloudtools`` is released under the MIT license, a copy of which can be
found in ``LICENSE``.
