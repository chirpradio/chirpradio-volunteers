#!/bin/sh
export PYTHONPATH=./site-packages
export CHIRP_EMAIL_HOST=email_host_when_testing
export CHIRP_EMAIL_PORT=9999
export CHIRP_EMAIL_HOST_PASSWORD=email_passwd_when_testing
export CHIRP_EMAIL_HOST_USER=email_user_when_testing
export CHIRP_EMAIL_HOST=email_host_when_testing
python2.7 chirp/manage.py test volunteers $@