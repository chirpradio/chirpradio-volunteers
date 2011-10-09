
begin;
alter table "volunteers_volunteer" add column "dj_shift_day" varchar(10) NOT NULL default "";
alter table "volunteers_volunteer" add column "dj_shift_time_slot" varchar(20) NOT NULL default "";
commit;