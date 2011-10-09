begin;

delete from auth_group_permissions where group_id = (select id from auth_group where name='Meeting Coordinator');
delete from auth_group where name='Meeting Coordinator';

commit;