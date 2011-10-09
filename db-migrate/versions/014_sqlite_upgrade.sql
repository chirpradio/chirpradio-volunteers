-- adds the event table and foreign key
begin;
CREATE TABLE "volunteers_event" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "location" varchar(200) NOT NULL,
    "start_date" date NULL,
    "duration_days" integer NOT NULL
)
;
alter table volunteers_task 
    add column "for_event_id" integer NULL REFERENCES "volunteers_event" ("id");
CREATE INDEX "volunteers_task_for_event_id" ON "volunteers_task" ("for_event_id");
commit;