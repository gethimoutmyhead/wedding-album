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

eventID = 0
sqlCall = 'SELECT * FROM events'
z = cur.execute(sqlCall)
result = z.fetchall()
for event in result:
	print (event)

eventID = int(input('Choose an event:'))
if ((eventID) and (eventID > 0) and (eventID <= len(result))):
	print (f'you chose {eventID}')
else:
	print('choice out of bounds, exiting')
	exit()

sqlCall = f'SELECT event_name, event_URL FROM events WHERE event_id = {eventID}'
z = cur.execute(sqlCall)
result = z.fetchall()

event_name = result[0][0]
event_url = result[0][1]

template = env.get_template('elit1.jinja')
outputPath = 'test_static/'
outputHTML_filename = f'{event_url}.html'

onlineURLForImages = 'https://s3.ap-southeast-1.amazonaws.com/shashi-and-trisha-wedd.ing/'
localURLForImages = dbs.basePathForPhotos

imageOutputPath = onlineURLForImages

theCall = f'''SELECT scaledPhotos.sourcePhoto_id, scaledPhotos.URL, facesInPhotos.face_id, faces.face_name 
	FROM scaledPhotos 
	JOIN photos ON scaledPhotos.sourcePhoto_id = photos.photo_id 
	JOIN facesInPhotos ON photos.photo_id = facesInPhotos.photo_id 
	JOIN faces on faces.face_id = facesInPhotos.face_id 
	WHERE photos.event_id = {eventID} and scaledPhotos.scaled_width = 500 
	ORDER BY photos.photo_filename ASC'''

sqlCall = theCall
z = cur.execute(sqlCall)
photoList = z.fetchall()


photoListInDict = []
for index, photo in enumerate(photoList):
	smallPhotoURL = photo[1]
	if(imageOutputPath == onlineURLForImages):
		smallPhotoURL = photo[1].replace(" ", "+")
	fullURLSmall = f"{imageOutputPath}{smallPhotoURL}"

	sqlCall = f"SELECT scaledPhotos.URL FROM scaledPhotos WHERE scaledPhotos.sourcePhoto_id = {photo[0]} AND scaledPhotos.scaled_width = 1200"
	z = cur.execute(sqlCall)
	result = z.fetchall()
	if result:
		bigPhotoURL = result[0][0]
		if(imageOutputPath == onlineURLForImages):
			bigPhotoURL = result[0][0].replace(" ", "+")
		fullURLBig = f"{imageOutputPath}{bigPhotoURL}"
	else:
		fullURLBig = fullURLSmall
	photoListInDict += [{'smallurl': fullURLSmall, 'bigurl': fullURLBig, 'bindex': index}]



#print (photoColumn1)
# rendering the template and storing the resultant text in variable output
myNewHeader = {"title": f"Photos of {event_name}", "headline": f"{event_name}"}
output = template.render(headerstuff = myNewHeader, picList = photoListInDict)

# printing the output on screen
# print(output)

with open(f"{outputPath}{outputHTML_filename}", 'w') as f:
    print(output, file = f)