# Execute the command on the server. Save the output to SQLlite database and query it.

from paramiko import SSHClient
import sqlite3
import paramiko
import re
import datetime
now = datetime.datetime.now()
client = SSHClient()
#client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("server.domain.com", username="username",password="yyyyy")
stdin, stdout, stderr = client.exec_command('ls -ltra')
print "stderr: ", stderr.readlines()
#print "pwd: ", stdout.readlines()
conn = sqlite3.connect('example.db')
c = conn.cursor()
for output in stdout.readlines():
    #print output.rstrip()
    data = re.sub('\s+', ' ', output.rstrip(), flags=0).split(' ')
    #print data
    if len(data) != 9:
        print "short"
    elif len(data) == 9:
        dirfilelink = data[0][0] 
        dirfilelink = 'f' if dirfilelink == '-' else dirfilelink
        fidonknow = data[1]
        fuserid = data[2]
        fgroup = data[3]
        fsize = data[4]
        fmonth = data[5]
        fday = data[6]
        fyear = data[7]
        fyear = now.year if fyear.find(':') else fyear
        fname = data[8]
        insert_SQL = "INSERT INTO files1 VALUES ('{dirfilelink}','{fidonknow}','{fuserid}','{fgroup}',{fsize},'{fmonth}',{fday},{fyear},'{fname}')"
        insert_SQL = insert_SQL.format(dirfilelink=dirfilelink,fidonknow=fidonknow,fuserid=fuserid,fgroup=fgroup,fsize = fsize,fmonth=fmonth,fday=fday,fyear=fyear,fname=fname)
        #print output
        #print insert_SQL
        c.execute(insert_SQL)

conn.commit()
for row in c.execute('SELECT * FROM files1 ORDER BY fsize'):
        print row        
conn.close()
