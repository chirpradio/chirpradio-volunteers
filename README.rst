=======================
CHIRP Volunteer Tracker
=======================

This is a website written in `Django`_ for administering `CHIRP`_ radio
station volunteers.

.. contents::

Users
=====

**Volunteer Coordinator**
    Assigns and approves tasks for volunteers
 
**Volunteer**
    Performs tasks for CHIRP radio
 
**Meeting Coordinator**
    Tracks attendance for CHIRP meetings

Developers
==========

Getting Started
---------------

To get started, first install `Python`_ 2.7.  We currently don't support
other versions of Python.  Check out the code from github::

  git clone git://github.com/chirpradio/chirpradio-volunteers.git

All dependencies are included in that checkout in the directory
``site-packages``. To be sure everything is installed and working, run the
tests for all installed apps::

    cd chirpradio-volunteers
    ./run_tests.sh

To start developing, first initialize the database (when it prompts you,
create a superuser to login as)::

    ./manage.sh syncdb

Then start the development server::

    ./manage.sh runserver

Browse to http://127.0.0.1:8000/ and login as the superuser you just created.

Using A Test DB
---------------

If you want to work with some real data, grab a test version of the database
which has been extracted at some point from production. You should check with
`some admins`_ to make sure this isn't too far out of date.

.. note::
    
    Be sure to check that it's not too far out of date. Run ``./dbmanage
    db_version`` and compare that with ``./dbmanage version``. If it is out of
    date run an upgrade on it per instructions below in the migration section.

Fire up a development server with the new database like this::

    ./manage.sh runserver

Browse to http://127.0.0.1:8000/ and login with one of the logins below.

Database Migrations
-------------------

To make any schema change to the database, you need to use the database
migration tools that live in the folder ``db-migrate``. The migrate and
sqlalchemy packages are required for this so be sure you have set the
PYTHONPATH in your shell like::

    export PYTHONPATH=./site-packages

If you just created a new db in the steps above, you will need to initialize
it like this::

    ./dbmanage.py version_control

You will only need to run that command once. From then on, check the version
of the database with this command::
    
    ./dbmanage.py db_version

And check the version of the script repository with this::
    
    ./dbmanage.py version

If the database is behind, upgrade it with this command::
    
    ./dbmanage.py upgrade

To create a new migration script, run::

    ./dbmanage.py script_sql sqlite

This will create two scripts: ./db-migrate/versions/xxx_sqlite_upgrade.sql and
./db-migrate/versions/xxx_sqlite_downgrade.sql respectively. Edit those
scripts with the new SQL and run the ``upgrade`` command again.

Migration Tips
--------------

If you want to add a new table or a new column just make the adjustments to the `Django Models`_ in chirp/volunteers/models.py (or wherever) and run something like this to see the new SQL ::
    
    ./manage.sh sqlall volunteers | less

Then you can copy / paste what you need into the upgrade script.
Unfortunately, you cannot drop columns with an alter statement in sqlite. To
work around this you have to create a temporary table, insert old data, then
replace the old table. See ``db-migrate/versions/009_sqlite_upgrade.sql`` for
an example.

If you are adding a new table and that table should be made available for
administration, you have to manually insert data for permissions to work. This
is because syncdb calls a custom function
``django/contrib/auth/management/__init__.py:create_permissions()`` but the
migration scripts do not [currently] call syncdb. Instead you can perform the
same SQL insert statements without too much trouble. See
``015_sqlite_upgrade.sql`` for an example of adding the event table to the
database.

.. _Django Models: http://docs.djangoproject.com/en/dev/topics/db/models/

Sending Email
-------------

You can develop local code that might send email by running a debugging SMTP
server. Start this up in a shell ::
    
    python2.7 -m smtpd -n -c DebuggingServer

then start the Django development server with a settings file that changes the
email port ::
    
    ./manage.sh runserver --settings=chirp.settings_dev

You should see the email text get logged to the shell you started the
debugging server on.

Hacking
-------

Use the `Project Tracker <http://code.google.com/p/chirpradio/>`_ for each
feature you add. Add tests for each feature. They are currently located in the
``chirp/volunteers/tests`` directory.

Community
---------

Feel free to get in touch with us on the `chirp-dev`_ mailing list with
questions or comments.


.. _Python: http://python.org/
.. _CHIRP: http://chicagoindependentradioproject.org/
.. _Django: http://www.djangoproject.com/
.. _Django 1.0: http://www.djangoproject.com/download/
.. _your IP address: http://whatismyip.org/
.. _serve your repository: http://hgbook.red-bean.com/hgbookch6.html#x10-1220006.4
.. _`some admins`: http://groups.google.com/group/chirpdev
.. _`chirp-dev`: http://groups.google.com/group/chirpdev
