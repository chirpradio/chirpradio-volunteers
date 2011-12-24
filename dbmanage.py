#!/usr/bin/env python2.7

"""Run this script to manage database schema upgrades

Example::

    $ export PYTHONPATH=./site-packages
    $ ./dbmanage.py --help

See README.txt for details.

"""

import os
from migrate.versioning.shell import main

here_dir = os.path.dirname(__file__)
main(
    url='sqlite:///%s' % os.path.abspath(os.path.join(here_dir, 'chirp', 'chirp.db')),
    repository='./db-migrate/')
