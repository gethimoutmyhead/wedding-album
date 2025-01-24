from jinja2 import Environment, FileSystemLoader
import sqlite3
import main_dbsettings as dbs
import json
# loading the environment
env = Environment(loader = FileSystemLoader('templates'))

# loading the template

con = sqlite3.connect(dbs.photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

personID = 40

sqlCall = '''SELECT face_id from faces 
	WHERE face_name NOT LIKE \'%blob%\' 
	AND face_name NOT LIKE \'%blur%\' 
	AND face_name NOT LIKE \'%profile%\' 
	AND face_name NOT LIKE \'%Person%\'
	ORDER BY face_name ASC'''
z = cur.execute(sqlCall)
result = z.fetchall()
personList = []
for person in result:
	personID = person[0]
	sqlCall = f'SELECT face_name, face_URL FROM faces WHERE face_id = {personID}'
	z = cur.execute(sqlCall)
	result = z.fetchall()
	face_name = result[0][0]
	face_url = result[0][1]
	print (f"building html for {face_name} to {face_url}" )
	personList += [{'faceURL': f"{face_url}.html", 'facename': face_name}]



template = env.get_template('elit_ppl_list.jinja')
outputPath = 'test_static/'
outputHTML_filename = f'people.html'
myNewHeader = {"title": f"Photos of Guests", "headline": f"Guests"}
output = template.render(headerstuff = myNewHeader, personList = personList)


with open(f"{outputPath}{outputHTML_filename}", 'w') as f:
	    print(output, file = f)