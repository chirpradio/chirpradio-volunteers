
begin;
alter table volunteers_volunteer add column "emergency_contact_name" varchar(50);
alter table volunteers_volunteer add column "emergency_contact_number" varchar(50);
alter table volunteers_volunteer add column "emergency_contact_relationship" varchar(50);
commit;