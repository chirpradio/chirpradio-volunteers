begin;
-- CREATE TABLE "django_content_type" (
--     "id" integer NOT NULL PRIMARY KEY,
--     "name" varchar(100) NOT NULL,
--     "app_label" varchar(100) NOT NULL,
--     "model" varchar(100) NOT NULL,
--     UNIQUE ("app_label", "model")
-- );
insert into django_content_type (name, app_label, model) 
    values ('task assignment', 'volunteers', 'taskassignment');
--     CREATE TABLE "auth_permission" (
--     "id" integer NOT NULL PRIMARY KEY,
--     "name" varchar(50) NOT NULL,
--     "content_type_id" integer NOT NULL,
--     "codename" varchar(100) NOT NULL,
--     UNIQUE ("content_type_id", "codename")
-- );
insert into auth_permission 
    select null as id, "Can add task assignment", id as content_type_id, "add_taskassignment" 
        from django_content_type where model='taskassignment';
insert into auth_permission 
    select null as id, "Can change task assignment", id as content_type_id, "change_taskassignment" 
        from django_content_type where model='taskassignment';
insert into auth_permission 
    select null as id, "Can delete task assignment", id as content_type_id, "delete_taskassignment" 
        from django_content_type where model='taskassignment';
        
--     CREATE TABLE "auth_group_permissions" (
--     "id" integer NOT NULL PRIMARY KEY,
--     "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
--     "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
--     UNIQUE ("group_id", "permission_id")
-- );
insert into auth_group_permissions (group_id, permission_id) values (
    (select id from auth_group where name = 'Volunteer Coordinator'),
    (select id from auth_permission where codename='add_taskassignment'));
insert into auth_group_permissions (group_id, permission_id) values (
    (select id from auth_group where name = 'Volunteer Coordinator'),
    (select id from auth_permission where codename='change_taskassignment'));
insert into auth_group_permissions (group_id, permission_id) values (
    (select id from auth_group where name = 'Volunteer Coordinator'),
    (select id from auth_permission where codename='delete_taskassignment'));

commit;