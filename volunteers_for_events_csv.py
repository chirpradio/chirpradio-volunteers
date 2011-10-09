
# script to output csv file of volunteers
# so it can be printed out for an event.
# this should probably become an option on 
# the site
import sqlite3
import csv
import sys
from cStringIO import StringIO

def main():
    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()
    c.execute("""
        select e.name, u.first_name, u.last_name, u.email, 
        v.phone_1, v.phone_2, v.emergency_contact_number,
        v.emergency_contact_relationship, 
        tt.short_description as task, 
        tt.description as task_details, 
        date(t.start_time) as day,
        time(t.start_time) as start_time, t.duration_minutes 
        from volunteers_taskassignment ta
        join volunteers_task t on t.id=ta.task_id
        join volunteers_tasktype tt on tt.id=t.task_type_id 
        join volunteers_volunteer v on ta.volunteer_id=v.id
        join auth_user u on u.id=v.user_id
        join volunteers_event e on t.for_event_id=e.id
        where e.start_date >= current_timestamp
        order by e.name, t.start_time
        """)
    fields = [d[0] for d in c.description]
    buf = StringIO()
    wtr = csv.writer(buf)
    wtr.writerow(fields)
    for row in c:
        wtr.writerow(row)
    print buf.getvalue()

if __name__ == '__main__':
    main()
