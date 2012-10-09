
import datetime
from datetime import timedelta
import re
from django.utils.translation import ugettext_lazy as _
from django.template import loader
from django import forms
from chirp.volunteers.models import User, Volunteer, TaskStatus, Event
from django.db import transaction
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site

class ResetPasswordForm(forms.Form):
    """
    A form that lets a volunteer user change reset his/her password
    based on email address.
    """
    email = forms.CharField(label=_("Email"), widget=forms.TextInput)
    new_password1 = forms.CharField(label=_("New password"),
                                            widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                            widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        # lookup user by email:
        # self.user = user
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        q = User.objects.filter(email=email)
        if q.count()==0:
            raise forms.ValidationError(_(
                "No user exists with that email.  Please ask "
                "volunteers@chirpradio.org to add you to the volunteer tracker."))
        else:
            matching_users = q.all()
            if len(matching_users) > 1:
                raise forms.ValidationError(_(
                    "Email belongs to multiple users.  Please ask "
                    "volunteers@chirpradio.org to reset your password manually."))

            self.user = matching_users[0]
        return email

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self):

        current_site = Site.objects.get_current()

        transaction.enter_transaction_management()
        transaction.managed(True)
        try:
            try:
                self.user.set_password(self.cleaned_data['new_password1'])
                self.user.save()
                message = loader.render_to_string('reset_password_email.txt', {
                    'user': self.user,
                    'raw_password': self.cleaned_data['new_password1'],
                    'full_server_url': 'http://%s/' % current_site.domain
                })
                msg = EmailMessage(
                        subject='New password for CHIRP Volunteer Tracker',
                        body=message,
                        to=[self.user.email]
                )
                msg.send(fail_silently=False)
            except:
                transaction.rollback()
                raise
            else:
                transaction.commit()
        finally:
            transaction.leave_transaction_management()

        return self.user

class ManageTasksForm(forms.Form):

    def __init__(self, *args, **kw):
        super(ManageTasksForm, self).__init__(*args, **kw)

        choices = [(0, _("[any volunteer]"))] # first selection choice
        for v in Volunteer.objects.all().order_by('user__first_name'):
            choices.append((v.id, "%s %s" % (v.user.first_name, v.user.last_name)))
        self['volunteer'].field.choices = choices

        choices = [(0, _("[any event]"))] # first selection choice
        for e in Event.objects.all().order_by('name', '-start_date'):
            choices.append((e.id, e))
        self['event'].field.choices = choices

        choices = [(0, _("[status]"))]
        for s in TaskStatus.objects.all().order_by('status'):
            choices.append((s.id, s.status))
        self['set_status_for_all'].field.choices = choices

    volunteer = forms.ChoiceField()
    event = forms.ChoiceField()
    set_status_for_all = forms.ChoiceField()
    show_completed = forms.BooleanField()
    show_canceled = forms.BooleanField()
    show_unassigned = forms.BooleanField()

def next_month(curdatetime):
    """Returns a datetime set to the first of the next month closest to curdatetime."""
    m = curdatetime.date().month
    adjusted_m = m
    while adjusted_m == m:
        curdatetime = curdatetime + timedelta(weeks=1)
        adjusted_m = curdatetime.date().month
    return curdatetime.replace(day=1)

class VolunteerActivityForm(forms.Form):

    def __init__(self, *args, **kw):
        super(VolunteerActivityForm, self).__init__(*args, **kw)

        choices = []
        # make a range that starts a year ago, to give enough time
        # to calculate past activity
        curdatetime = datetime.datetime.now() - timedelta(weeks=52)
        now = datetime.datetime.now()
        while curdatetime < now:
            curmonth = curdatetime.date()
            choices.append((curmonth.strftime("%Y-%m-01"), curmonth.strftime("%b 1st, %Y")))
            curdatetime = next_month(curdatetime)

        self['as_of_date'].field.choices = choices

    def clean_as_of_date(self):
        as_of_date = self.cleaned_data['as_of_date']
        # can only be a date like 2009-01-01
        return re.sub(r'[^0-9-]', '', as_of_date)

    as_of_date = forms.ChoiceField()


class CloneEventForm(forms.Form):
    existing_event = forms.ChoiceField()
    new_name = forms.CharField()
    new_start_date = forms.DateField(initial=datetime.date.today)

    def __init__(self, *args, **kw):
        super(CloneEventForm, self).__init__(*args, **kw)
        choices = [(e.id, e.short_name()) for e in
                   Event.objects.all().order_by('name', '-start_date')]
        self['existing_event'].field.choices = choices
