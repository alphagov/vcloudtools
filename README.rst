vcloudtools
===========

A set of commandline utilities to aid working with the VMWare vCloud API. 

Installation
------------

For the time being, I suggest you clone the repository, and do a::

    $ pip install -e .

Usage
-----

Simple usage::

    $ eval `vcloud-login`
    $ vcloud-org list
    $ vcloud-org show <ORG NAME>

License
-------

``vcloudtools`` is released under the MIT license, a copy of which can be found
in ``LICENSE``.
