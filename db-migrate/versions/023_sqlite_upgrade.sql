begin;
alter table volunteers_event add column "tasks_can_be_claimed" bool NOT NULL default 0;
update volunteers_event set tasks_can_be_claimed=1;
commit;