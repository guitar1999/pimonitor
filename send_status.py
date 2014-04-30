#!/usr/bin/python

import argparse, ConfigParser, psycopg2

config = ConfigParser.RawConfigParser()
config.read('/home/jessebishop/.pyconfig')
dbhost = config.get('wfdb', 'DBHOST')
dbname = config.get('wfdb', 'DBNAME')
dbuser = config.get('wfdb', 'DBUSER')

p = argparse.ArgumentParser(prog="send_status.py")
p.add_argument('-p', '--piname', dest="piname", required=True, help="The name of the pi being monitored.")
args = p.parse_args()

db = psycopg2.connect(host=dbhost, database=dbname, user=dbuser)
cursor = db.cursor()

query = """UPDATE pi_checkin SET timestamp = CURRENT_TIMESTAMP WHERE pi = '{0}';""".format(args.piname)
try:
    cursor.execute(query)
    db.commit()
except Exception, msg:
    print msg
cursor.close()
db.close()

