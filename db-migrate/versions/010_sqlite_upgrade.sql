begin;
alter table volunteers_volunteer add column "dues_waived" bool NOT NULL default false;
commit;