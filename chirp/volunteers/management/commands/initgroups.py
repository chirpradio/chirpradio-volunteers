
"""Creates initial auth groups needed for volunteers app. 

Run this after creating a fresh db with `python manage.py syncdb`
"""

from django.core.management.base import NoArgsCommand

def initgroups(quiet=False):    
    from django.contrib.auth.models import Group, Permission
    
    perms = Permission.objects.filter(codename__in=[
        'add_user',
        'change_user',
        'delete_user',
        'add_committee',
        'change_committee',
        'delete_committee',
        'add_task',
        'change_task',
        'delete_task',
        'add_tasktype',
        'change_tasktype',
        'delete_tasktype',
        'add_volunteer',
        'change_volunteer',
        'delete_volunteer',
        'add_taskassignment',
        'change_taskassignment',
        'delete_taskassignment',
        ])
    vol = Group(name="Volunteer Coordinator")
    vol.save()
    for p in perms:
        vol.permissions.add(p)
    assert vol._get_pk_val()==1, (
        "*sigh* due to fixture loading, the Volunteer Coordinator Group ID must be 1")
    if not quiet:
        print "Created Volunteer Coordinator Group"
        
    perms = Permission.objects.filter(codename__in=[
        'add_task',
        'change_task',
        'change_volunteer',
        ])
    vol = Group(name="Volunteer")
    vol.save()
    for p in perms:
        vol.permissions.add(p)
    assert vol._get_pk_val()==2, (
        "*sigh* due to fixture loading, the Volunteer Group ID must be 2")
    if not quiet:
        print "Created Volunteer Group"
        
    perms = Permission.objects.filter(codename__in=[
        'add_meeting',
        'change_meeting',
        'change_meeting',
        ])
    vol = Group(name="Meeting Coordinator")
    vol.save()
    for p in perms:
        vol.permissions.add(p)
    assert vol._get_pk_val()==3, (
        "*sigh* due to fixture loading, the Volunteer Group ID must be 3")
    if not quiet:
        print "Created Meeting Coordinator Group"

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = __doc__
    
    def handle_noargs(self, **options):
        initgroups()
        