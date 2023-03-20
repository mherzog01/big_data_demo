import sqlite3
import pandas as pd
import csv

metadb_path = 'meta.db'

con = sqlite3.connect(metadb_path)
cur = con.cursor()

print()
print('Tables and columns')
# https://stackoverflow.com/a/41007154/11262633
newline_indent = '\n   '
con.text_factory = str

result = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
table_names = sorted(list(zip(*result))[0])
print ("\ntables are:"+newline_indent+newline_indent.join(table_names))

for table_name in table_names:
    result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
    column_names = list(zip(*result))[1]
    print (("\ncolumn names for %s:" % table_name)
                      +newline_indent
                      +(newline_indent.join(column_names)))


print()
print('Read records')
sql = 'select * from meta'
res = con.execute(sql).fetchmany(10)
print(res)

print()
print('Display  with headers')
df = pd.read_sql_query('select * from meta limit 10', con)
print(df.iloc[:3])

# Fails on the CloudShell computer - crashes - memory issue?
#print()
#print('Export with headers - reading')
#df = pd.read_sql_query('select * from meta', con)
#print('Exporting')
#df.write_csv('meta.csv')

print()
print('Work around memory issue')
sql = 'select * from meta'

# THe following crashes with a memory error
#res = con.execute(sql).fetchall()
with open('meta.csv', 'w', newline='') as f:
    # using csv.writer method from csv module
    write = csv.writer(f)
    #print(column_names)
    #print(result)
    write.writerow([str(v) for v in column_names])
    cur = con.execute(sql)
    num_rows = 0
    while True:
        row = cur.fetchone()
        if not row:
            break
        num_rows += 1
        if num_rows % 1000000 == 0:
            print(num_rows)
        write.writerow([str(v) for v in row])

print (f"Complete.  Rows={num_rows}")
