from jinja2 import Environment, FileSystemLoader
import sqlite3
import main_dbsettings as dbs
import json
# loading the environment
env = Environment(loader = FileSystemLoader('templates'))

# loading the template
template = env.get_template('elit1.jinja')
outputPath = 'test_static/'
outputHTML_filename = 'Kieran_D.html'
outputJS_filename = 'Kieran_D.js'
onlineURLForImages = 'https://s3.ap-southeast-1.amazonaws.com/shashi-and-trisha-wedd.ing/'
localURLForImages = dbs.basePathForPhotos

imageOutputPath = onlineURLForImages
con = sqlite3.connect(dbs.photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

theCall = '''SELECT scaledPhotos.sourcePhoto_id, scaledPhotos.URL, photos.event_ID 
	from scaledPhotos
	JOIN photos ON scaledPhotos.sourcePhoto_id = photos.photo_id
	WHERE scaledPhotos.scaled_width = 1200 AND photos.event_ID = 3'''

theCall = '''SELECT scaledPhotos.sourcePhoto_id, scaledPhotos.URL, facesInPhotos.face_id, faces.face_name 
	FROM scaledPhotos 
	JOIN photos ON scaledPhotos.sourcePhoto_id = photos.photo_id 
	JOIN facesInPhotos ON photos.photo_id = facesInPhotos.photo_id 
	JOIN faces on faces.face_id = facesInPhotos.face_id 
	WHERE faces.face_id = 40 and scaledPhotos.scaled_width = 1200'''

sqlCall = theCall
z = cur.execute(sqlCall)
photoList = z.fetchall()


photoListInDict = []
for index, photo in enumerate(photoList):
	z = photo[1]
	if(imageOutputPath == onlineURLForImages):
		z = photo[1].replace(" ", "+")

	fullURL = f"{imageOutputPath}{z}"
	photoListInDict.append({'index': photo[0], 'URL': fullURL})

photoListInJSON = json.dumps(photoListInDict)
outputText = f"gallery = {photoListInJSON}"

with open(f"{outputPath}{outputJS_filename}", "w") as textfile:
	textfile.write(outputText)

theCall = '''SELECT scaledPhotos.sourcePhoto_id, scaledPhotos.URL, facesInPhotos.face_id, faces.face_name 
	FROM scaledPhotos 
	JOIN photos ON scaledPhotos.sourcePhoto_id = photos.photo_id 
	JOIN facesInPhotos ON photos.photo_id = facesInPhotos.photo_id 
	JOIN faces on faces.face_id = facesInPhotos.face_id 
	WHERE faces.face_id = 40 and scaledPhotos.scaled_width = 500 ORDER BY ((facesInPhotos.faceInPhoto_right_abs - facesInPhotos.faceInPhoto_left_abs) * (facesInPhotos.faceInPhoto_bottom_abs - facesInPhotos.faceInPhoto_top_abs)) DESC'''

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


# photoColumn1 = [{'burl': 'cheese'},{'burl': 'Chess'}]

photoColumn1 = photoListInDict[::3]
photoColumn2 = photoListInDict[1::3]
photoColumn3 = photoListInDict[2::3]

#print (photoColumn1)
# rendering the template and storing the resultant text in variable output
myNewHeader = {"title": "The groovy page", "JSPhotoList": outputJS_filename, "headline": "the first page"}
output = template.render(headerstuff = myNewHeader, picList = photoListInDict)

# printing the output on screen
# print(output)

with open(f"{outputPath}{outputHTML_filename}", 'w') as f:
    print(output, file = f)