import mysql.connector
import datetime

def logmsg(p_msg):
    print(p_msg)
    
def logmsg01(p_msg):
    logmsg(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}: {p_msg}')
    
logmsg01('Process begins')
with open('/home/ec2-user/.my.cnf') as f:
    for line in f.readlines():
        if line[:8] == "password":
            pw = line[9:].replace('"','').strip()

cnx = mysql.connector.connect(user='admin', 
                              password=pw,
                              host='demo-db-1.cq2s02rjdpvt.us-east-1.rds.amazonaws.com',
                              port=3306,
                              database='scale_aws')

cursor = cnx.cursor()

query = ("delete from demo_scale")

logmsg01('Deleting....')
cursor.execute(query)
cnx.commit()

logmsg01('Inserting....')


for i in range(10000):
    query = f"insert into demo_scale values (current_timestamp(),'{str(i)}')"
    #print(query)
    cursor.execute(query)
    #break
cnx.commit()


cursor.execute('select count(*) ct from demo_scale')
for row in cursor:
    print(f'# rows={row}')
    break

logmsg01('Done')

cursor.close()
cnx.close()