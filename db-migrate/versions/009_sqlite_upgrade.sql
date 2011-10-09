-- removes the Completed boolean column from Task Assignment table:
begin;
create temporary table tsk_asn_backup(
    "id" integer NOT NULL PRIMARY KEY,
    "task_id" integer NOT NULL REFERENCES "volunteers_task" ("id"),
    "volunteer_id" integer NOT NULL REFERENCES "volunteers_volunteer" ("id"),
    "points" integer NOT NULL,
    "status_id" integer NOT NULL REFERENCES "volunteers_taskstatus" ("id"),
    "established" datetime NOT NULL,
    "modified" datetime NOT NULL
);
insert into tsk_asn_backup select id, task_id, volunteer_id, points, status_id, established, modified from volunteers_taskassignment;
drop table volunteers_taskassignment;
CREATE TABLE "volunteers_taskassignment" (
    "id" integer NOT NULL PRIMARY KEY,
    "task_id" integer NOT NULL REFERENCES "volunteers_task" ("id"),
    "volunteer_id" integer NOT NULL REFERENCES "volunteers_volunteer" ("id"),
    "points" integer NOT NULL,
    "status_id" integer NOT NULL REFERENCES "volunteers_taskstatus" ("id"),
    "established" datetime NOT NULL,
    "modified" datetime NOT NULL
);
insert into volunteers_taskassignment select * from tsk_asn_backup;
CREATE INDEX "volunteers_taskassignment_task_id" ON "volunteers_taskassignment" ("task_id");
CREATE INDEX "volunteers_taskassignment_volunteer_id" ON "volunteers_taskassignment" ("volunteer_id");
CREATE INDEX "volunteers_taskassignment_status_id" ON "volunteers_taskassignment" ("status_id");

drop table tsk_asn_backup;
commit;