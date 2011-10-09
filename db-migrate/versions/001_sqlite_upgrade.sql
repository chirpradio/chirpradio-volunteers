
begin;
alter table "volunteers_volunteer" add column "phone_1" varchar(20) NOT NULL default "";
alter table "volunteers_volunteer" add column "phone_2" varchar(20) NOT NULL default "";
commit;