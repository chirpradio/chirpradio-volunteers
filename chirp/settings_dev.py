
"""A settings file for local development"""

from chirp.settings import *

# 
# start:
#   python -m smtpd -n -c DebuggingServer
#
# then you can watch email headers
# 
EMAIL_PORT=8025