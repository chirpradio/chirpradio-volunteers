
-- Adds tables for meeting tracking
BEGIN;
CREATE TABLE "volunteers_meeting" (
    "id" integer NOT NULL PRIMARY KEY,
    "meeting_date" date NOT NULL,
    "established" datetime NOT NULL,
    "modified" datetime NOT NULL
)
;
CREATE TABLE "volunteers_meeting_attendees" (
    "id" integer NOT NULL PRIMARY KEY,
    "meeting_id" integer NOT NULL REFERENCES "volunteers_meeting" ("id"),
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    UNIQUE ("meeting_id", "user_id")
)
;
COMMIT;