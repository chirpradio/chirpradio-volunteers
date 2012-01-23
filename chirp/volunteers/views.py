
import datetime
from datetime import timedelta
import urllib
from decimal import Decimal
from django.template import Context, loader, RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db import transaction, connection
from django import forms
from django.shortcuts import render_to_response, get_object_or_404
from chirp.utils import as_json
from chirp.volunteers.models import (
        User, Meeting, Event, Task, TaskStatus, Volunteer, TaskAssignment)
from django.contrib import auth
from django.contrib.auth.models import Group
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.functional import wraps
from django.utils.dateformat import format as dateformat, time_format
from chirp.volunteers.forms import (ResetPasswordForm, ManageTasksForm,
                                    VolunteerActivityForm, CloneEventForm)
from django.core.mail import EmailMessage
import csv
from StringIO import StringIO
from django.contrib import admin

# A decorator that passes its function if the user is a member of the
# specified group. Otherwise, redirect to /. Usage:
#
# @ifusergroup('Volunteer')
# ...
class ifusergroup :
    def __init__(self, group) :
        self.group = group

    def __call__(self, func) :
        def wrapper(request, *args, **kwargs) :
            try :
                group = Group.objects.get(name=self.group)
            except Group.DoesNotExist :
                return HttpResponseRedirect('/')
            
            if group in request.user.groups.all() :
                return func(request, *args, **kwargs)

            return HttpResponseRedirect('/')
   
        return wraps(func)(wrapper)

@staff_member_required
def admin_index(request):
    ctx = {'volunteer_activity_form': VolunteerActivityForm(),
           'clone_event_form': CloneEventForm()}
    return admin.site.index(request, extra_context=ctx)

@staff_member_required
@ifusergroup('Meeting Coordinator')
def meetings(request):
    t = loader.get_template('meetings.html')
    c = Context({
        'title':'Meeting Attendance Tracker',
        'user': auth.get_user(request),
        'root_path': '/' # just for the admin logout page
    })
    return HttpResponse(t.render(c))

@staff_member_required
@ifusergroup('Meeting Coordinator')
@as_json
def add_meeting_attendee(request, meeting_id, user_id):
    m = Meeting.objects.get(id=meeting_id)
    user = User.objects.get(id=user_id)
    q = Volunteer.objects.filter(user=user)
    if not q.count():
        raise ValueError("Cannot add attendee user %r because he/she is not a volunteer" % user)
    m.attendees.add(user)
    m.save()
    return {
        'success':True
    }
    
@staff_member_required
@ifusergroup('Meeting Coordinator')
@as_json
def delete_meeting_attendee(request, meeting_id, user_id):
    m = Meeting.objects.get(id=meeting_id)
    m.attendees.remove(User.objects.get(id=user_id))
    m.save()
    return {
        'success':True
    }

@staff_member_required
@ifusergroup('Meeting Coordinator')
@as_json
def track_meeting(request, mon, day, year):
    # this should add or edit a meeting:
    meeting_date = datetime.date( int(year), int(mon), int(day) )
    q = Meeting.objects.filter(meeting_date=meeting_date)
    count = q.count()
    if count == 1:
        meeting = q[0]
    elif count == 0:
        meeting = Meeting(meeting_date=meeting_date)
        meeting.save()
    else:
        raise RuntimeError("Somehow there are %s meetings on %s" % (count, meeting_date))
        
    return {
        'meeting_id': meeting.id,
        'attendees': [dict(user_id=u.id, name=(u.first_name + " " + u.last_name)) 
                        for u in meeting.attendees.all()]
    }

@staff_member_required
@ifusergroup('Volunteer')
def show_tasks_for_claiming(request):
    t = loader.get_template('claim_tasks.html')
    events = [e for e in Event.objects.all().order_by("start_date")]
    current_events = []
    now_date = datetime.datetime.now().date()
    for ev in events:
        # hide old events ...
        if ev.start_date + timedelta(days=ev.duration_days) >= now_date:
            current_events.append(ev)
    
    c = Context({
        'events': current_events,
        'title':'Claim A Task',
        'user': auth.get_user(request),
        'root_path': '/' # just for the admin logout page
    })
    return HttpResponse(t.render(c))
    
@staff_member_required
@ifusergroup('Volunteer')
@transaction.commit_manually
@as_json
def claim_task(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
        # note that due to how sqlite begins transactions in deferred 
        # mode by default (can we fix this?) there is a slight chance 
        # that two people can claim a task at once.  In case that happens, 
        # there is a bit of added protection here so more people can't claim it.
        if len(task.claimed_by) >= task.num_volunteers_needed:
            return {
                'success': False,
                'error': "All volunteers needed for this task have been filled (%s)" % task
            }
        current_user = auth.get_user(request)
        try:
            volunteer = Volunteer.objects.get(user=current_user)
        except Volunteer.DoesNotExist, exc:
            raise ValueError(
                "%s (%s) is not a volunteer.  An admin needs to create a volunteer "
                "record and link it to this user." % (
                    current_user, current_user.get_full_name()))
        if current_user in task.claimed_by:
            return {
                'success': False,
                'error': "You have already claimed this task (%s)" % (
                                                        task.__unicode__())
            } 
        assignment = TaskAssignment()
        assignment.task = task
        assignment.volunteer = volunteer
        if task.potential_points:
            assignment.points = task.potential_points
        else:
            assignment.points = Decimal('1')
        assignment.save()
        
        template_vars = {'event' : task.for_event,
                         'task'  : task}
        message = loader.render_to_string('claim_task_email.txt', template_vars)
        msg = EmailMessage(subject='You have volunteered for a CHIRP task.',
                           body=message,
                           to=[current_user.email])
        msg.send(fail_silently=False)
    except:
        transaction.rollback()
        raise
    else:
        transaction.commit()

    return {'success': True,
            'user': {
                'first_name': current_user.first_name, 
                'last_name': current_user.last_name
                }}

def password_change_done(request):
    return render_to_response("password_change_done.html")
    
def password_change(request, template_name='password_change_form.html',
                    post_change_redirect=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('chirp.volunteers.views.password_change_done')
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = ResetPasswordForm()
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

@staff_member_required
def search_users(request):
    ulist = []
    for user in User.objects.filter(
                    first_name__startswith=request.GET['q']
                                    ).all():
        ulist.append("%s %s|%s" % (
                    user.first_name, user.last_name, 
                    user.id))
                    
    return HttpResponse("\n".join(ulist))

@staff_member_required
@ifusergroup('Volunteer Coordinator')
def manage_tasks(request, template_name="manage_tasks.html"):
    if request.GET:
        tasks_requested = True
        form = ManageTasksForm(request.GET)
        if int(request.GET.get('event', 0)):
            event = Event.objects.get(pk=request.GET.get('event'))
        else:
            event = None
        if request.GET.get('show_unassigned') == 'on':
            query = (Task.objects.filter(taskassignment=None)
                     .order_by('-for_event__start_date', '-start_time'))
            if not event:
                raise ValueError('You must select an event when viewing '
                                 'unassigned tasks.')
            query = query.filter(for_event=event)
        else:
            query = (TaskAssignment.objects
                     .order_by('-task__for_event__start_date',
                               '-task__start_time'))
            if event:
                query = query.filter(task__for_event=event)
            # when checkboxes are *not* checked then exclude these status:
            if request.GET.get('show_completed', False) != 'on':
                query = query.exclude(status__status="Completed")
            if request.GET.get('show_canceled', False) != 'on':
                # needs db migration to fix this:
                query = query.exclude(status__status="Cancelled")
            if int(request.GET.get('volunteer',0)):
                query = query.filter(   volunteer__id=request.GET['volunteer'],
                                        volunteer__user__is_staff=True,
                                        volunteer__user__is_active=True)
    else:
        event = None
        tasks_requested = False
        form = ManageTasksForm()
        query = []
        
    task_assignments = []
    if len(query):
        choices = [(s.id, s.status) for s in TaskStatus.objects.all().order_by('status')]
        for ob in query:
            if request.GET.get('show_unassigned', False) == 'on':
                task = ob
                task_assignments.append({
                    'status_select': '',
                    'assignment': None,
                    'task': task,
                    'edit_assignment_href': None,
                    'edit_task_href': '/volunteers/task/%s/' % task.id
                })
            else:
                assignment = ob
                name = "status__%s" % (assignment.id)
                value = assignment.status.id
                status_select = forms.ChoiceField(choices=choices)
                task_assignments.append({
                    'status_select': status_select.widget.render(name, value, attrs={'class': 'status'}),
                    'assignment': assignment,
                    'task': assignment.task,
                    'edit_assignment_href': '/volunteers/taskassignment/%s/' % assignment.id,
                    'edit_task_href': '/volunteers/task/%s/' % assignment.task.id
                })

    if event:
        event_edit_href = '/volunteers/event/%s/' % event.id
    else:
        event_edit_href = None
    return render_to_response(template_name, {
        'form': form,
        'task_assignments': task_assignments,
        'tasks_requested': tasks_requested,
        'volunteer_id': request.GET.get('volunteer', 0),
        'event_id': request.GET.get('event', 0),
        'event_edit_href': event_edit_href,
        'show_completed': request.GET.get('show_completed','') and 'on',
        'show_canceled': request.GET.get('show_canceled','') and 'on'
    }, context_instance=RequestContext(request))

@staff_member_required
@ifusergroup('Volunteer Coordinator')
def manage_tasks_save_changes(request):
    if not request.POST:
        return HttpResponseForbidden()
    
    for key,val in request.POST.iteritems():
        if key.startswith('status'):
            # e.g. status__2 meaning task assignment of ID 2
            task_assignment = TaskAssignment.objects.get(id=key.split('__')[1])
            task_assignment.status = TaskStatus.objects.get(id=val)
            task_assignment.save()
            
    query_params = [
        ('volunteer', request.POST['volunteer']),
        ('event', request.POST['event'])]
    if request.POST.get('show_completed',False) == 'on':
        query_params.append(('show_completed', 'on'))
    if request.POST.get('show_canceled',False) == 'on':
        query_params.append(('show_canceled', 'on'))
    return HttpResponseRedirect('/chirp/tasks/manage/?%s' % urllib.urlencode(query_params))


@staff_member_required
@ifusergroup('Volunteer Coordinator')
def clone_event(request):
    if not request.POST:
        return HttpResponseForbidden()
    event = Event.objects.get(pk=request.POST['existing_event'])
    new_event = Event(name=request.POST['new_name'],
                      location=event.location,
                      tasks_can_be_claimed=False,
                      start_date=request.POST['new_start_date'],
                      duration_days=event.duration_days)
    new_event.save()
    for t in event.task_set.all():
        new_event.task_set.create(
                        for_event=new_event,
                        for_committee=t.for_committee,
                        task_type=t.task_type,
                        start_time=t.start_time,
                        duration_minutes=t.duration_minutes,
                        num_volunteers_needed=t.num_volunteers_needed,
                        potential_points=t.potential_points,
                        description=t.description)
    new_event.save()
    query_params = [('event', new_event.id),
                    ('volunteer', 0), # all volunteers
                    ('show_unassigned', 'on')]
    return HttpResponseRedirect('/chirp/tasks/manage/?%s'
                                % urllib.urlencode(query_params))


@staff_member_required
@ifusergroup('Volunteer Coordinator')
def get_csv_of_all_volunteers(request):
    c = connection.cursor()
    c.execute("""
        select u.first_name, u.last_name, u.email, 
        v.phone_1, v.phone_2, v.emergency_contact_number,
        v.emergency_contact_relationship 
        from volunteers_volunteer v
        join auth_user u on u.id=v.user_id
        where u.is_active
        """)
    fields = [d[0] for d in c.description]
    buf = StringIO()
    wtr = csv.writer(buf)
    wtr.writerow(fields)
    for row in c:
        wtr.writerow(row)
    return HttpResponse(buf.getvalue(), mimetype='text/csv')

@staff_member_required
@ifusergroup('Volunteer Coordinator')
def get_csv_of_volunteers_with_unpaid_dues(request):
    c = connection.cursor()
    c.execute("""
        select u.first_name, u.last_name, u.email, %(year)s as year
        from volunteers_volunteer v
        join auth_user u on u.id=v.user_id
        where u.is_active
        and v.dues_paid_year != %(year)s
        """ % {'year': repr(datetime.datetime.now().strftime("%Y"))})
    fields = [d[0] for d in c.description]
    buf = StringIO()
    wtr = csv.writer(buf)
    wtr.writerow(fields)
    for row in c:
        wtr.writerow(row)
    return HttpResponse(buf.getvalue(), mimetype='text/csv')

@staff_member_required
@ifusergroup('Volunteer Coordinator')
def get_csv_of_volunteer_activity(request):
    form = VolunteerActivityForm(request.GET)
    if not form.is_valid():
        raise ValueError("form is not valid")

    user_points = {}
    for v in Volunteer.objects.filter(user__is_active=True).all():
        user_points.setdefault("%s %s" % (v.user.first_name, v.user.last_name), 0)
    
    c = connection.cursor()
    c.execute("""
        select 
        u.first_name, u.last_name, sum(asn.points) as points 
    from 
        volunteers_taskassignment asn 
        join volunteers_taskstatus st on st.id=asn.status_id 
        join volunteers_task t on t.id=asn.task_id 
        join volunteers_tasktype tt on tt.id=t.task_type_id 
        left join volunteers_event e on e.id=t.for_event_id 
        join volunteers_volunteer v on v.id=asn.volunteer_id 
        join auth_user u on u.id=v.user_id 
    where u.is_active and st.status = 'Completed' and asn.modified >= %s
    group by 1, 2
        """, [form.cleaned_data['as_of_date']])
        
    fields = [d[0] for d in c.description]
    for row in c:
        r = dict(zip(fields, row))
        user_points["%s %s" % (r['first_name'], r['last_name'])] += Decimal(str(r['points']))
        
    c.execute("""
    select 
        u.first_name, u.last_name, 1 as points 
    from 
        volunteers_meeting_attendees a 
        join volunteers_meeting m on m.id=a.meeting_id 
        join auth_user u on u.id=a.user_id
        join volunteers_volunteer v on u.id=v.user_id
    
    where u.is_active and m.meeting_date >= %s
    """, [form.cleaned_data['as_of_date']])
        
    fields = [d[0] for d in c.description]
    for row in c:
        r = dict(zip(fields, row))
        user_points["%s %s" % (r['first_name'], r['last_name'])] += Decimal(str(r['points']))
    
    buf = StringIO()
    wtr = csv.writer(buf)
    wtr.writerow(['volunteer', 'points since %s' % form.cleaned_data['as_of_date']])
    for volunteer, points in user_points.iteritems():
        wtr.writerow([volunteer, points])
    
    return HttpResponse(buf.getvalue(), mimetype='text/csv')
