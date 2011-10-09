
begin;
alter table volunteers_volunteer drop column "discovered_chirp_by";
alter table volunteers_volunteer drop column "discovered_chirp_by_details";
commit;