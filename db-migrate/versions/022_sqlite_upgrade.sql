begin;
alter table volunteers_volunteer add column "emergency_contact_email" varchar(75) NOT NULL default "";
commit;