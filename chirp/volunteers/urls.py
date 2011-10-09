
"""URLs for the Volunteers app.

Note that the prefix to these URLs is http://.../chirp/
"""

from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^password_change/?$',
        'chirp.volunteers.views.password_change'),
    (r'^password_change_done/?$',
        'chirp.volunteers.views.password_change_done'),
    (r'^meetings/?$', 
        'chirp.volunteers.views.meetings'),
    (r'^meetings/(\d+)/attendee/add/(\d+)\.json$', 
        'chirp.volunteers.views.add_meeting_attendee'),
    (r'^meetings/(\d+)/attendee/delete/(\d+)\.json$', 
        'chirp.volunteers.views.delete_meeting_attendee'),
    (r'^meetings/(\d{2})/(\d{2})/(\d{4})/track\.json$', 
        'chirp.volunteers.views.track_meeting'),
    (r'^search_users/?$', 
        'chirp.volunteers.views.search_users'),
    (r'^tasks/manage/save_changes/?$', 
        'chirp.volunteers.views.manage_tasks_save_changes'),
    (r'^tasks/manage/?$', 
        'chirp.volunteers.views.manage_tasks'),
    (r'^tasks/clone-event/?$', 
        'chirp.volunteers.views.clone_event'),
    (r'^tasks/claim/(\d+)\.json$', 
        'chirp.volunteers.views.claim_task'),
    (r'^tasks/claim/?$', 
        'chirp.volunteers.views.show_tasks_for_claiming'),
    (r'^chirp_all_volunteers\.csv$', 
        'chirp.volunteers.views.get_csv_of_all_volunteers'),
    (r'^chirp_volunteers_unpaid_dues\.csv$', 
        'chirp.volunteers.views.get_csv_of_volunteers_with_unpaid_dues'),
    (r'^chirp_volunteer_activity\.csv$',
        'chirp.volunteers.views.get_csv_of_volunteer_activity'),
)

if settings.ENABLE_TEST_URLS:
    urlpatterns += patterns('',
        (r'^_ui_test_/claim_tasks_dev/?$', 
            'chirp.volunteers._ui_test_.claim_tasks.claim_tasks_dev'),
        (r'^_ui_test_/meetings_dev/?$', 
            'chirp.volunteers._ui_test_.meetings.meetings_dev'),
        (r'^_ui_test_/meetings_test/?$', 
            'chirp.volunteers._ui_test_.meetings.meetings_test'),
    )