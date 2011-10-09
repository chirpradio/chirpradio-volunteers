
"""Django settings for chirp project.

This file is read by Django to configure the website.
"""

import os
HERE_DIR = os.path.abspath(os.path.dirname(__file__))

# Debug will show tracebacks in the browser:
DEBUG = True

# Enable special URLs that are only used for testing the UI
ENABLE_TEST_URLS = True

TEMPLATE_DEBUG = DEBUG
PROJECT_ROOT_DIR = HERE_DIR

# Email for where production errors get sent, etc
ADMINS = (
    ('Kumar McMillan', 'kumar.mcmillan@gmail.com'),
)

MANAGERS = ADMINS

# Used by django.core.mail.EmailMessage()
DEFAULT_FROM_EMAIL = ADMINS[0][1] # email of 1st admin

# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_ENGINE = 'sqlite3'           
# Or path to database file if using sqlite3.
DATABASE_NAME = os.path.join(HERE_DIR, 'chirp.db')
# Not used with sqlite3.
DATABASE_USER = ''             
# Not used with sqlite3.
DATABASE_PASSWORD = ''         
# Set to empty string for localhost. Not used with sqlite3.
DATABASE_HOST = ''             
# Set to empty string for default. Not used with sqlite3.
DATABASE_PORT = ''
# Increases the database timeout to better handle lock contention.
# For more information, please see
# http://groups.google.com/group/django-developers/browse_thread/thread/d320de970c2a4016?fwc=1
DATABASE_OPTIONS = {'timeout': 30}

# temporary workaround for buggy :memory: test db, but slower.
# seemed to creep in when using pysqlite over sqlite3.
# see http://www.mail-archive.com/django-users@googlegroups.com/msg62359.html
TEST_DATABASE_NAME = "/tmp/chirp-%s-test.db" % os.environ.get('USER','anon')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# ID for this site, only necessary when using sites contrib
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
# NOTE: this must be different on the production server, 
# do not commit to version control what is used in production
SECRET_KEY = '70!e5sko&f)co3d39w4^*qkff-im7*p0(jh)*luygo)wpma=#p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

# Middleware installed for this application.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

# Path to module that defines URL mapping
ROOT_URLCONF = 'chirp.urls'

# Directory paths where templates are defined
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" 
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(HERE_DIR, 'templates'),
)

# List of installed applications for this site.
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'chirp.volunteers',
)

# For testing and during the dump/load data manage.py commands, 
# fixture data sets can be found in these directories.
FIXTURE_DIRS = (
    os.path.join(HERE_DIR, 'fixtures'),
    os.path.join(HERE_DIR, 'volunteers', 'tests', 'fixtures'),
)

EMAIL_HOST = os.environ['CHIRP_EMAIL_HOST']
EMAIL_HOST_USER = os.environ['CHIRP_EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['CHIRP_EMAIL_HOST_PASSWORD']
EMAIL_PORT = int(os.environ['CHIRP_EMAIL_PORT'])
EMAIL_USE_TLS = True
