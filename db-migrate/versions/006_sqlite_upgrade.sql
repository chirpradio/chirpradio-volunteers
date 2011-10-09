begin;

CREATE TABLE "volunteers_task_tmp" (
    "id" integer NOT NULL PRIMARY KEY,
    "for_committee_id" integer NOT NULL REFERENCES "volunteers_committee" ("id"),
    "task_type_id" integer NOT NULL REFERENCES "volunteers_tasktype" ("id"),
    "description" text NOT NULL,
    "established" datetime NOT NULL,
    "modified" datetime NOT NULL
);

insert into volunteers_task_tmp select id, for_committee_id, task_type_id, description, established, modified from volunteers_task;

CREATE TABLE "volunteers_taskassignment" (
    "id" integer NOT NULL PRIMARY KEY,
    "task_id" integer NOT NULL REFERENCES "volunteers_task" ("id"),
    "volunteer_id" integer NOT NULL REFERENCES "volunteers_volunteer" ("id"),
    "points" integer NOT NULL,
    "status_id" integer NOT NULL REFERENCES "volunteers_taskstatus" ("id"),
    "completed" bool NOT NULL,
    "established" datetime NOT NULL,
    "modified" datetime NOT NULL
);

insert into volunteers_taskassignment select null as id, id as task_id, volunteer_id, points, status_id, completed, established, modified from volunteers_task;

drop table volunteers_task;   
alter table volunteers_task_tmp rename to volunteers_task;

CREATE INDEX "volunteers_task_for_committee_id" ON "volunteers_task" ("for_committee_id");
CREATE INDEX "volunteers_task_task_type_id" ON "volunteers_task" ("task_type_id");
CREATE INDEX "volunteers_taskassignment_task_id" ON "volunteers_taskassignment" ("task_id");
CREATE INDEX "volunteers_taskassignment_volunteer_id" ON "volunteers_taskassignment" ("volunteer_id");
CREATE INDEX "volunteers_taskassignment_status_id" ON "volunteers_taskassignment" ("status_id");

commit;