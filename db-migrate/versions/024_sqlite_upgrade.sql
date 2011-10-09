begin;

insert into auth_group (name) values ('Meeting Coordinator');

-- adds permissions for Volunteer Coordinator
insert into auth_group_permissions (group_id, permission_id) values (
    (select id from auth_group where name = 'Meeting Coordinator'), 
    (select id from auth_permission where codename = "add_event"));
insert into auth_group_permissions (group_id, permission_id) values (
    (select id from auth_group where name = 'Meeting Coordinator'), 
    (select id from auth_permission where codename = "change_event"));
insert into auth_group_permissions (group_id, permission_id) values (
    (select id from auth_group where name = 'Meeting Coordinator'), 
    (select id from auth_permission where codename = "delete_event"));
    
commit;