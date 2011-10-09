begin;

-- change type of potential_points from integer to decimal
create temporary table volunteers_task_backup 
    as select * from volunteers_task;
drop table volunteers_task;

CREATE TABLE "volunteers_task" (
    "id" integer NOT NULL PRIMARY KEY,
    "for_committee_id" integer NOT NULL REFERENCES "volunteers_committee" ("id"),
    "for_event_id" integer NULL REFERENCES "volunteers_event" ("id"),
    "task_type_id" integer NOT NULL REFERENCES "volunteers_tasktype" ("id"),
    "start_time" datetime NULL,
    "duration_minutes" integer NULL,
    "num_volunteers_needed" smallint unsigned NULL,
    "potential_points" decimal NULL,
    "description" text NOT NULL,
    "established" datetime NOT NULL,
    "modified" datetime NOT NULL
)
;

insert into volunteers_task select 
    id,
    for_committee_id,
    for_event_id,
    task_type_id,
    start_time,
    duration_minutes,
    num_volunteers_needed,
    potential_points,
    description,
    established,
    modified
    from volunteers_task_backup;
    
CREATE INDEX "volunteers_task_for_committee_id" ON "volunteers_task" ("for_committee_id");
CREATE INDEX "volunteers_task_for_event_id" ON "volunteers_task" ("for_event_id");
CREATE INDEX "volunteers_task_task_type_id" ON "volunteers_task" ("task_type_id");

drop table volunteers_task_backup;

-- change type of points from integer to decimal
create temporary table volunteers_taskassignment_backup 
    as select * from volunteers_taskassignment;
drop table volunteers_taskassignment;

CREATE TABLE "volunteers_taskassignment" (
    "id" integer NOT NULL PRIMARY KEY,
    "task_id" integer NOT NULL REFERENCES "volunteers_task" ("id"),
    "volunteer_id" integer NOT NULL REFERENCES "volunteers_volunteer" ("id"),
    "points" decimal NOT NULL,
    "status_id" integer NOT NULL REFERENCES "volunteers_taskstatus" ("id"),
    "established" datetime NOT NULL,
    "modified" datetime NOT NULL
)
;

insert into volunteers_taskassignment select 
    id,
    task_id,
    volunteer_id,
    points,
    status_id,
    established,
    modified
    from volunteers_taskassignment_backup;

CREATE INDEX "volunteers_taskassignment_task_id" ON "volunteers_taskassignment" ("task_id");
CREATE INDEX "volunteers_taskassignment_volunteer_id" ON "volunteers_taskassignment" ("volunteer_id");
CREATE INDEX "volunteers_taskassignment_status_id" ON "volunteers_taskassignment" ("status_id");

drop table volunteers_taskassignment_backup;

commit;