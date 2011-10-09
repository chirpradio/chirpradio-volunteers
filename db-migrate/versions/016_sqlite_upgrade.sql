begin;
-- whoops, forgot to add these columns in migration 014
alter table volunteers_task 
    add column "start_time" datetime NULL;
alter table volunteers_task 
    add column "duration_minutes" integer NULL;
alter table volunteers_task 
    add column "num_volunteers_needed" smallint unsigned NULL;
commit;