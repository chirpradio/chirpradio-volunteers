begin;

-- adds event content type
insert into django_content_type (name, app_label, model) values (
    "event", "volunteers", "event");

-- adds permissions for event table
insert into auth_permission (name, content_type_id, codename) values (
    "Can add event",
    (select id from django_content_type where app_label="volunteers" and model="event"),
    "add_event"
    );
insert into auth_permission (name, content_type_id, codename) values (
    "Can change event",
    (select id from django_content_type where app_label="volunteers" and model="event"),
    "change_event"
    );
insert into auth_permission (name, content_type_id, codename) values (
    "Can delete event",
    (select id from django_content_type where app_label="volunteers" and model="event"),
    "delete_event"
    );

-- adds permissions for Volunteer Coordinator
insert into auth_group_permissions (group_id, permission_id) values (
    (select id from auth_group where name = 'Volunteer Coordinator'), 
    (select id from auth_permission where codename = "add_event"));
insert into auth_group_permissions (group_id, permission_id) values (
    (select id from auth_group where name = 'Volunteer Coordinator'), 
    (select id from auth_permission where codename = "change_event"));
insert into auth_group_permissions (group_id, permission_id) values (
    (select id from auth_group where name = 'Volunteer Coordinator'), 
    (select id from auth_permission where codename = "delete_event"));

commit;