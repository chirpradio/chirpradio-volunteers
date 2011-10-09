
begin;
alter table "volunteers_volunteer" add column "vol_info_sheet" bool NOT NULL default false;
commit;