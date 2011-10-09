
# script to output csv file of all volunteers
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
        select u.first_name, u.last_name, u.email, 
        v.phone_1, v.phone_2, v.emergency_contact_number,
        v.emergency_contact_relationship 
        from volunteers_volunteer v
        join auth_user u on u.id=v.user_id
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
