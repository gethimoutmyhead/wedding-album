import sqlite3
import main_dbsettings as dbs

con = sqlite3.connect(dbs.photoAlbum_DB)
cur = con.cursor()

cur.execute('PRAGMA foreign_keys = ON')

sqlCall = '''SELECT * from faces 
	WHERE face_name NOT LIKE \'%blob%\' 
	AND face_name NOT LIKE \'%blur%\' 
	AND face_name NOT LIKE \'%profile%\' 
	AND face_name NOT LIKE \'%Person%\'
	ORDER BY face_name ASC'''
z = cur.execute(sqlCall)
result = z.fetchall()

for a in result:
	print (a)

print (len(result))