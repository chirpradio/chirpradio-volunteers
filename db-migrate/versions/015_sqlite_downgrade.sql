begin;
delete from django_content_type where 
    name="event" and app_label="volunteers" and model="event";
delete from auth_permission where codename = "add_event";
delete from auth_permission where codename = "change_event";
delete from auth_permission where codename = "delete_event";
    
delete from auth_group_permissions where
    group_id = (select id from auth_group where name = 'Volunteer Coordinator') and
    permission_id = (select id from auth_permission where codename = "add_event");
delete from auth_group_permissions where
    group_id = (select id from auth_group where name = 'Volunteer Coordinator') and
    permission_id = (select id from auth_permission where codename = "change_event");
delete from auth_group_permissions where
    group_id = (select id from auth_group where name = 'Volunteer Coordinator') and
    permission_id = (select id from auth_permission where codename = "delete_event");
    
commit;