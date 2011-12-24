
"""base testing components"""

from django.contrib.admin.sites import LOGIN_FORM_KEY
from django.contrib.auth import models as auth_models
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.test import TestCase

from chirp.volunteers.models import User

def eq_(value, expected_value):
    assert value==expected_value, (
        "%r != %r" % (value, expected_value))


class BaseTest(TestCase):

    def setUp(self):
        super(BaseTest, self).setUp()
        def noop(*a, **kw):
            return True
        # Sigh. After upgrading from Python 2.5 to 2.7, logging into the
        # admin via tests wasn't working in Django 1.1. I tried to do it the
        # right way which you can uncomment below. In the meantime, this
        # makes an anonymous user look like our desired authenticated user.
        def LoggedInUser(*args, **kw):
            qs = self._get_user()
            user = qs[0]
            user.is_authenticated = noop
            return user
        auth_models.AnonymousUser = LoggedInUser


class CoordinatorLoginTest(BaseTest):

    def setUp(self):
        super(CoordinatorLoginTest, self).setUp()
        # resp = self.client.get('/')
        # login = self.client.post('/', {
        #     REDIRECT_FIELD_NAME: '/',
        #     LOGIN_FORM_KEY: 1,
        #     'username': 'coordtest',
        #     'password': 'test',
        # })
        # self.assertRedirects(login, '/')
        # assert self.client.login(username='coordtest', password='test')

    def _get_user(self):
        return User.objects.filter(username='coordtest')

    def tearDown(self):
        super(CoordinatorLoginTest, self).tearDown()
        # self.client.logout()

class MeetingCoordLoginTest(BaseTest):

    def setUp(self):
        super(MeetingCoordLoginTest, self).setUp()
        # self.client.get('/')
        # login = self.client.post('/', {
        #     REDIRECT_FIELD_NAME: '/',
        #     LOGIN_FORM_KEY: 1,
        #     'username': 'meetingcoord',
        #     'password': 'test',
        # })
        # self.assertRedirects(login, '/')
        # assert self.client.login(username='meetingcoord', password='test')

    def _get_user(self):
        return User.objects.filter(username='meetingcoord')

    def tearDown(self):
        super(MeetingCoordLoginTest, self).tearDown()
        # self.client.logout()

class VolunteerLoginTest(BaseTest):

    def setUp(self):
        super(VolunteerLoginTest, self).setUp()
        # self.client.get('/')
        # login = self.client.post('/', {
        #     REDIRECT_FIELD_NAME: '/',
        #     LOGIN_FORM_KEY: 1,
        #     'username': 'volunteertest',
        #     'password': 'test',
        # })
        # self.assertRedirects(login, '/')
        # assert self.client.login(username='volunteertest', password='test') # True if can login

    def _get_user(self):
        return User.objects.filter(username='volunteertest')

    def tearDown(self):
        super(VolunteerLoginTest, self).tearDown()
        # self.client.logout()
