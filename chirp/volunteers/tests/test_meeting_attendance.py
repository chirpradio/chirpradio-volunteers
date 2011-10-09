
import datetime
from django.utils import simplejson
from chirp.volunteers.models import Meeting, User
from chirp.volunteers.tests.base import eq_, MeetingCoordLoginTest
from django.contrib.auth.models import User

class JsonResponseException(Exception):
    """An exception was raised in a JSON handler."""

class TestMeetingAttendance(MeetingCoordLoginTest):
    
    fixtures = ['users.json', 'volunteers.json', 'meetings.json']
    
    def assertValidJson(self, response):
        eq_(response['content-type'], 'application/json')
        data = simplejson.loads(response.content)
        if 'error' in data:
            raise JsonResponseException(data['error'])
    
    def test_new_meeting(self):
        resp = self.client.get('/chirp/meetings/02/05/2009/track.json')
        eq_(resp.status_code, 200)
        data = simplejson.loads(resp.content)
        eq_(data['attendees'], [])
        
        meeting = Meeting.objects.get(id=data['meeting_id'])
        eq_(meeting.meeting_date.timetuple()[0:3], (2009,2,5))
    
    def test_add_attendee(self):
        
        meeting = Meeting.objects.get(meeting_date=datetime.date(2009,3,1))
        
        a1 = User.objects.get(username='meeting_attendee_1')
        resp = self.client.get('/chirp/meetings/%s/attendee/add/%s.json' % (
                                                            meeting.id, a1.id))
        eq_(resp.status_code, 200)
        data = simplejson.loads(resp.content)
        eq_(data['success'],True)
        
        a2 = User.objects.get(username='meeting_attendee_2')
        resp = self.client.get('/chirp/meetings/%s/attendee/add/%s.json' % (
                                                            meeting.id, a2.id))
        eq_(resp.status_code, 200)
        data = simplejson.loads(resp.content)
        eq_(data['success'],True)
        
        eq_(sorted([a.first_name for a in meeting.attendees.all()]), ['Bob','Jenny'])
    
    def test_cannot_add_non_volunteer_attendee(self):
        
        meeting = Meeting.objects.get(meeting_date=datetime.date(2009,3,1))
        
        # cannot add a user if user is not a volunteer:
        henry = User(username='henry', first_name="Henry", last_name="Blanch")
        henry.save()
        
        def add_non_volunteer_user():
            resp = self.client.get('/chirp/meetings/%s/attendee/add/%s.json' % (
                                                            meeting.id, henry.id))
            self.assertValidJson(resp)
        
        self.assertRaises(JsonResponseException, add_non_volunteer_user)
        
    def test_delete_attendee(self):
        
        meeting = Meeting.objects.get(meeting_date=datetime.date(2009,3,1))
        
        a1 = User.objects.get(username='meeting_attendee_1')
        resp = self.client.get('/chirp/meetings/%s/attendee/add/%s.json' % (
                                                            meeting.id, a1.id))
        eq_(resp.status_code, 200)
        data = simplejson.loads(resp.content)
        eq_(data['success'],True)
        
        eq_([a.first_name for a in meeting.attendees.all()], ['Bob'])
        
        resp = self.client.get('/chirp/meetings/%s/attendee/delete/%s.json' % (
                                                            meeting.id, a1.id))
        eq_(resp.status_code, 200)
        data = simplejson.loads(resp.content)
        eq_(data['success'],True)
        
        eq_([a.first_name for a in meeting.attendees.all()], [])
    
    def test_search_users(self):
        resp = self.client.get('/chirp/search_users', {'q':'b'})
        eq_(resp.status_code, 200)
        data = sorted(resp.content.split("\n"))
        eq_(data, ['Bob Hope|6'])
        
        resp = self.client.get('/chirp/search_users', {'q':'Jenny'})
        eq_(resp.status_code, 200)
        data = sorted(resp.content.split("\n"))
        eq_(data, ['Jenny Craig|7'])
    
    ## hmm, this isn't implemented and it might not be so useful
    ## since autocomplete is fast
    
    # def test_search_users_fullname(self):
    #     resp = self.client.get('/chirp/search_users', {'q':'jenny craig'})
    #     eq_(resp.status_code, 200)
    #     data = sorted(resp.content.split("\n"))
    #     eq_(data, ['Jenny Craig|7'])
        
        