#!/usr/bin/python

import argparse, ConfigParser, psycopg2
from tweet import *

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

query = """SELECT (CURRENT_TIMESTAMP - timestamp) < interval '5 minutes' AS success, notified FROM pi_checkin WHERE pi = '{0}';""".format(args.piname)
try:
    cursor.execute(query)
    success, notified = cursor.fetchall()[0]
    if not success:
        if not notified:
            #send a tweet
            status = """Hey @jessebishop, {0} hasn't been heard from in over 5 minutes!""".format(args.piname)
            tweet(status)
            query = """UPDATE pi_checkin SET notified = TRUE WHERE pi = '{0}';""".format(args.piname)
            cursor.execute(query)
        else:
            query = """SELECT (CURRENT_TIMESTAMP - timestamp) > interval '1 day' AS check FROM pi_checkin WHERE pi = '{0}';""".format(args.piname)
            cursor.execute(query)
            check = cursor.fetchall()[0][0]
            if check:
                status = """Hey @jessebishop, {0} hasn't been heard from in over a day!""".format(args.piname)
                tweet(status)
                query = """UPDATE pi_checkin SET timestamp = CURRENT_TIMESTAMP - interval '6 minutes' WHERE pi = '{0}';""".format(args.piname)
                cursor.execute(query)
    else:
        query = """UPDATE pi_checkin SET notified = FALSE WHERE pi = '{0}'""".format(args.piname)
        cursor.execute(query)
except Exception, msg:
    print msg
cursor.close()
db.close()

