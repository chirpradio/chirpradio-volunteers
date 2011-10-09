
"""Data model"""

from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.db.models import signals
from django.utils.dateformat import format as dateformat, time_format

__all__ = ['Volunteer', 'Task', 'TaskAssignment', 'TaskStatus', 'TaskType', 'Committee', 'Event']


class Committee(models.Model):
    """A CHIRP committee that a Volunteer belongs to."""
    
    name = models.CharField(max_length=100)
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name


def get_dues_paid_year_choices():
    """Returns choices for the Dues Paid form field.
    
    Returns tuple of tuples.  I.E. ::
            
        (('2007', '2007'), ('2008', '2008'))
        
    """
    years = []
    y = int(datetime.now().strftime('%Y'))
    while y >= 2008:
        years.append((str(y),str(y)))
        y = y - 1 
    return years

    
class Volunteer(models.Model):
    """A volunteer user"""
    
    user = models.ForeignKey(User, verbose_name="volunteer user",
            help_text=("""\
            To add a new user go to the Home page and click Add next to Users 
            in the Auth panel.  After creating a new user, 
            <strong>be sure</strong> you do the following.  Under Personal 
            Details, enter first name, last name, and email address.  Under 
            Permissions, check the box Staff status.  Under Groups, add the 
            new user to the group Volunteer. Then come back to this screen 
            and select the user."""))
    committees = models.ManyToManyField(Committee, 
        verbose_name="active in these committees",
        blank=True,
        help_text="""\
            Click the plus sign to add a new committee or go to Home > Volunteers > 
            Committees to edit the name of a committee.""")
    emergency_contact_name = models.CharField(max_length=50, blank=True)
    emergency_contact_email = models.EmailField(blank=True)
    emergency_contact_number = models.CharField(max_length=50, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    dj_shift_day = models.CharField(max_length=10, blank=True, choices=[
        ('mondays', 'Mondays'),
        ('tuesdays', 'Tuesdays'),
        ('wednesdays', 'Wednesdays'),
        ('thursdays', 'Thursdays'),
        ('fridays', 'Fridays'),
        ('saturdays', 'Saturdays'),
        ('sundays', 'Sundays'),
        ], 
        help_text="""\
            Select the day of this DJ's shift or leave it blank if the DJ is 
            not currently active.""")
    dj_shift_time_slot = models.CharField(max_length=20, blank=True, 
        help_text="""\
            Enter the time slot (i.e. 9pm - 12am) or leave it blank if the 
            DJ is not currently active.""")
    vol_info_sheet = models.BooleanField("volunteer info sheet on file")
    dues_paid_year = models.CharField("dues paid up to", max_length=4, blank=True, 
        choices=get_dues_paid_year_choices(),
        help_text="""\
        Select the year for which this volunteer last paid dues.  Leave it 
        blank if the volunteer has not paid any dues yet.  If a volunteer does 
        not have to pay dues, leave this blank and check the Dues Waived box 
        below.""")
    dues_waived = models.BooleanField(
                    "volunteer does not have to pay dues (waived)")
    phone_1 = models.CharField(max_length=20, blank=True)
    phone_2 = models.CharField(max_length=20, blank=True)
    address_line_1 = models.CharField(max_length=200, blank=True)
    address_line_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=80, default='Chicago', blank=True)
    state = models.CharField(max_length=2, default='IL', blank=True)
    day_job = models.CharField(max_length=250, blank=True)
    availability = models.CharField(max_length=200, blank=True, 
        help_text="""\
        Days and times this volunteer is generally available 
        (i.e. 'evenings')""")
    skills = models.TextField(blank=True, 
        help_text="""\
        Enter any special skills that might be useful to CHIRP""")
    has_a_car = models.BooleanField()
    has_equipment = models.BooleanField()
    can_dj_events = models.BooleanField("can DJ events")
    can_fix_stuff = models.BooleanField()
    knows_computers = models.BooleanField()
    resources = models.TextField("additional resources", blank=True,
        help_text="List any additional resources that might useful to CHIRP")
    
    discovered_chirp_by_choices = [
        'Friends',
        'CHIRP website',
        'Another website',
        'News article',
        'Record Fair',
        'WLUW',
        'Table at a Festival or Show',
        'Other'
    ]
    # re-format so that the value and prompts are the same:
    discovered_chirp_by_choices = [
        (txt.lower(), txt) for txt in discovered_chirp_by_choices
    ]
    discovered_chirp_by = models.CharField(
        max_length=100, 
        choices=discovered_chirp_by_choices, 
        blank=True,
        verbose_name="Discovered CHIRP by")
        
    discovered_chirp_by_details = models.CharField(
        max_length=200, blank=True,
        verbose_name="Details",
        help_text="""
        Name of website, friend, or festival (if applicable)
        """)
    
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s (%s %s)" % (self.user.username, 
                               self.user.first_name, 
                               self.user.last_name)
    
    def first_name(self):
        """returns volunteer's first name if available, otherwise username"""
        return self.user.first_name or self.user.username
            
    def last_name(self):
        """returns volunteer's last name"""
        return self.user.last_name
        
    def email(self):
        """returns volunteer's email address"""
        return self.user.email


class Event(models.Model):
    """Describes an event."""

    name = models.CharField(max_length=100, verbose_name='event name')
    location = models.CharField(max_length=200, verbose_name='event location')
    tasks_can_be_claimed = models.BooleanField(default=False, 
                                    verbose_name='tasks are ready to be claimed')
    start_date = models.DateField(blank=True, null=True,
                                  verbose_name='start date')
    DURATION_DAYS_CHOICES = (
        (1, '1 day'),
        (2, '2 days'),
        (3, '3 days'),
        (4, '4 days'),
        (5, '5 days'),
        )
    duration_days = models.IntegerField(default=1,
                                        choices=DURATION_DAYS_CHOICES,
                                        verbose_name='event duration')

    def __unicode__(self):
        if not self.start_date:
            return self.name
        if self.duration_days == 1:
            return '%s (%s)' % (self.name, self.start_date)
        return '%s (%d days, starts %s)' % (self.name, self.duration_days,
                                            self.start_date)

    def short_name(self, suffix='', maxlen=71):
        st = self.name
        if (len(st) + len(suffix)) > maxlen:
            st = '%s...' % (st[0:maxlen-3])
        return u'%s%s' % (st, suffix)
    
    @property
    def tasks(self):
        tasks = []
        if self.tasks_can_be_claimed:
            tasks = [t for t in self.task_set.all().order_by("start_time")]
        return tasks
    

class TaskStatus(models.Model):
    """The status of a task performed by a volunteer"""
    
    status = models.CharField(max_length=40)
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = verbose_name_plural = 'task status'
    
    def __unicode__(self):
        return self.status


class TaskType(models.Model):
    """The type of a task performed by a volunteer"""
    
    short_description = models.CharField(max_length=240)
    important_note = models.CharField(
            max_length=200, blank=True, null=True,
            help_text="""\
            Enter an important note about this 
            task type.  For example: "May require heavy lifting." """)
    description = models.TextField(blank=True)
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.short_description

    
class Task(models.Model):
    """The task performed by a volunteer.
    
    This task may be assigned multiple times
    """
    
    class Meta:
        ordering = ['-established']

    for_committee = models.ForeignKey(Committee)
    for_event = models.ForeignKey(Event, blank=True, null=True)
    task_type = models.ForeignKey(TaskType, verbose_name='type of task',
        help_text="""\
        Select what type of task this is or click the plus sign to 
        add a new task type.""")
    start_time = models.DateTimeField(blank=True, null=True,
                                      verbose_name='start time')
                                      
    DURATION_MINUTES_CHOICES = (
        (30, '1/2 hour'),
        (60, '1 hour'),
        (90, '1 1/2 hours'),
        (120, '2 hours'),
        (150, '2 1/2 hours'),
        (180, '3 hours'),
        (210, '3 1/2 hours'),
        (240, '4 hours'),
        (270, '4 1/2 hours'),
        (300, '5 hours'),
        (330, '5 1/2 hours'),
        (360, '6 hours'),
        (390, '6 1/2 hours'),
        )
    duration_minutes = models.IntegerField(blank=True, null=True,
                                           choices=DURATION_MINUTES_CHOICES,
                                           verbose_name='task duration')
    num_volunteers_needed = models.PositiveSmallIntegerField(
        blank=True, null=True, default=1,
        verbose_name='number of volunteers needed')
    potential_points = models.DecimalField(
        blank=True, null=True, max_digits=5, decimal_places=1,
        help_text="""
            Potential points that can be earned for this task.  Actual points 
            are set in the task assignment.
            """)
    description = models.TextField(blank=True, 
        help_text="""\
        A custom description for this task if it's different from the task type.""")
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    @property
    def claim_task_url(self):
        return "/chirp/tasks/claim/%s.json" % self.id
    
    @property
    def end_time(self):
        if not self.start_time or not self.duration_minutes:
            raise ValueError(
                "Cannot access self.end_time because this task does "
                "not have a start_time or duration value.")
        return self.start_time + timedelta(minutes=self.duration_minutes)
    
    @property
    def claim_prompt(self):
        return (
            "You are about to commit to %s." % self.__unicode__())
    
    @property
    def claimed_by(self):
        # return users assigned to this task (includes completed tasks)
        return [asn.volunteer.user for asn in 
                self.taskassignment_set.filter(
                        status__in=TaskStatus.objects.filter(
                                        status__in=['Assigned','Completed']))]
                            
    def __unicode__(self):
        task = self.task_type.__unicode__()
        descr = self.description or self.task_type.description
        if descr:
            task = "%s: %s" % (task, descr)
        if self.start_time:
            task = "%s on %s from %s - %s" % (
                        task, 
                        dateformat(self.start_time, "D M jS"),
                        time_format(self.start_time, "g:i a"),
                        time_format(self.end_time, "g:i a"))
            
        return task


class TaskAssignment(models.Model):
    """A task assigned to a Volunteer."""
    
    task = models.ForeignKey(Task,
        help_text="""\
        Select the task or click the plus sign to create a 
        new one.""")
    volunteer = models.ForeignKey(Volunteer, verbose_name="assigned to volunteer",
        help_text="""\
        Select a volunteer to perform this task or click the plus sign 
        to add a new one.""")
    points = models.DecimalField(
        max_digits=5, decimal_places=1,
        help_text="points that will be earned for this task")
    status = models.ForeignKey(TaskStatus, 
        default=lambda: TaskStatus.objects.filter(status='Assigned')[0])
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s assigned to %s" % (self.task.__unicode__(), 
                                      self.volunteer.__unicode__())

        
class Meeting(models.Model):
    meeting_date = models.DateField()
    attendees = models.ManyToManyField(User)
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    
    
