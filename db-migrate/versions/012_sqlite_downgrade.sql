
begin;
alter table volunteers_volunteer drop column emergency_contact_name;
alter table volunteers_volunteer drop column emergency_contact_number;
alter table volunteers_volunteer drop column emergency_contact_relationship;
commit;