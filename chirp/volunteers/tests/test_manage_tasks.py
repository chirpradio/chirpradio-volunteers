
"""tests managing volunteer tasks"""

import unittest
from chirp.volunteers.models import Volunteer, Committee, Task, TaskType, TaskAssignment, TaskStatus
from django.contrib.auth.models import User
from chirp.volunteers.tests.base import eq_, CoordinatorLoginTest

__all__ = ['TestManageTasks']
        
class TestManageTasks(CoordinatorLoginTest):
    
    fixtures = ['tasks_to_manage.json']
    
    def test_manage_tasks_context(self):
        
        resp = self.client.get('/chirp/tasks/manage/')
        context = resp.context[0]
        vol = Volunteer.objects.all().order_by("user__first_name")[0]
        eq_(context['form']['volunteer'].field.widget.choices[1][1], 
            "%s %s" % (vol.user.first_name, vol.user.last_name))
        eq_(0, len(context['task_assignments']))
    
    def test_manage_tasks_for_volunteer(self):
        
        resp = self.client.get('/chirp/tasks/manage/?volunteer=%s&show_canceled=on' % 2)
        context = resp.context[0]
        
        a = context['task_assignments'][0]
        eq_(str(a['assignment'].task), "Tabling: sell merch")
        
        a = context['task_assignments'][1]
        eq_(str(a['assignment'].task), "Tabling: sell swag")
        
        eq_(context['volunteer_id'], '2')
        eq_(context['event_id'], 0)
        eq_(context['show_completed'], '')
        eq_(context['show_canceled'], 'on')
    
    def test_manage_tasks_for_event(self):
        
        resp = self.client.get('/chirp/tasks/manage/?event=%s' % 1)
        context = resp.context[0]
        
        a = context['task_assignments'][0]
        eq_(str(a['assignment'].task), "Event Load In: load in")
        
        eq_(context['event_id'], '1')
        eq_(context['volunteer_id'], 0)
        eq_(context['show_completed'], '')
        eq_(context['show_canceled'], '')
    
    def test_update_task_status(self):
        
        completed = TaskStatus.objects.get(status="Completed").id
        resp = self.client.post('/chirp/tasks/manage/save_changes', {
            'volunteer': 2,
            'event': 0,
            'show_completed': 'on',
            # set two assignments to completed:
            'status__1': completed,
            'status__2': completed
        })
        redirect = '/chirp/tasks/manage/?volunteer=2&event=0&show_completed=on'
        self.assertRedirects(resp, redirect)
        resp = self.client.get(redirect)
        
        context = resp.context[0]
        
        a = context['task_assignments'][0]
        eq_(str(a['assignment'].status), "Completed")
        
        a = context['task_assignments'][1]
        eq_(str(a['assignment'].status), "Completed")
    
    def test_edit_hrefs(self):
        
        resp = self.client.get('/chirp/tasks/manage/?volunteer=%s' % 2)
        context = resp.context[0]
        
        a = context['task_assignments'][0]
        
        resp = self.client.get(a['edit_task_href'])
        eq_(resp.context[0]['title'], "Change task")
        
        resp = self.client.get(a['edit_assignment_href'])
        eq_(resp.context[0]['title'], "Change task assignment")
    
    def test_show_unassigned_tasks(self):
        
        completed = TaskAssignment.objects.all().delete()
        resp = self.client.get('/chirp/tasks/manage/', {
            'event': 1,
            'show_unassigned': 'on'
        })
        eq_(resp.status_code, 200)
        context = resp.context[0]

        a = context['task_assignments'][0]
        eq_(str(a['task']), "Event Load In: load in")
    
    def test_no_unassigned_tasks_to_show(self):
        resp = self.client.get('/chirp/tasks/manage/', {
            'event': 1,
            'show_unassigned': 'on'
        })
        eq_(resp.status_code, 200)
        context = resp.context[0]
        eq_(len(context['task_assignments']), 0)
