begin;
-- no data in yet
drop table "volunteers_task";
CREATE TABLE "volunteers_task" (
    "id" integer NOT NULL PRIMARY KEY,
    "volunteer_id" integer NOT NULL REFERENCES "volunteers_volunteer" ("id"),
    "for_committee_id" integer NOT NULL REFERENCES "volunteers_committee" ("id"),
    "points" integer NOT NULL,
    "task_type_id" integer NOT NULL REFERENCES "volunteers_tasktype" ("id"),
    "description" text NOT NULL,
    "completed" bool NOT NULL,
    "status_id" integer NOT NULL REFERENCES "volunteers_taskstatus" ("id"),
    "established" datetime NOT NULL,
    "modified" datetime NOT NULL
);
CREATE INDEX "volunteers_task_volunteer_id" ON "volunteers_task" ("volunteer_id");
CREATE INDEX "volunteers_task_for_committee_id" ON "volunteers_task" ("for_committee_id");
CREATE INDEX "volunteers_task_task_type_id" ON "volunteers_task" ("task_type_id");
CREATE INDEX "volunteers_task_status_id" ON "volunteers_task" ("status_id");
commit;