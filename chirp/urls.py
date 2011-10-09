
import os
from django.conf import settings

"""URL mapping for the chirp website.

All URLs point to the administrative interface.  For example, the 
URL to administer new task assignments for volunteers would be::

    /volunteers/taskassignment/
 
"""

from django.conf.urls.defaults import *

from django.contrib import admin
# Necessary to load modules from chirp.volunteers.admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^chirp/', include('chirp.volunteers.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    # this needs to be separate from admin media:
    (r'^local_site_media/(?P<path>.*)$', 
                    'django.views.static.serve', {
                        'show_indexes': True,
                        'document_root': os.path.join(settings.PROJECT_ROOT_DIR, 'media')
                    }),
    )

# route all other requests to admin:
urlpatterns += patterns('',
    (r'^$', 'chirp.volunteers.views.admin_index'), # special case
    (r'', include(admin.site.urls)),
)