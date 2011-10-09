
begin;
alter table "volunteers_volunteer" add column "dues_paid_year" varchar(4) NOT NULL default "";
commit;