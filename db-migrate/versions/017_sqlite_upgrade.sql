
-- revoking all admin editing permissions from Volunteer 
-- because we are providing a custom screen for Volunteer actions

delete from auth_group_permissions where group_id = (select id from auth_group where name = 'Volunteer');