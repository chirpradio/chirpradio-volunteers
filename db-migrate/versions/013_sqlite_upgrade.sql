
begin;
alter table volunteers_volunteer add column "discovered_chirp_by" varchar(100);
alter table volunteers_volunteer add column "discovered_chirp_by_details" varchar(50);
commit;