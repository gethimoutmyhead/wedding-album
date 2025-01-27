from jinja2 import Environment, FileSystemLoader
import sqlite3
import main_dbsettings as dbs
import json
import os
# loading the environment
env = Environment(loader = FileSystemLoader('templates'))

# loading the template

con = sqlite3.connect(dbs.photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

baseURLForFrontEnd = "/Users/shashithuryrajaponraja/dev-projects/face-detect/static/"
baseURLForPhotos = "/Users/Shared/Wedding stuff/Photos/"
subDirectoryForOutput = "admin/people/"
outputDirectory_full = f"{baseURLForFrontEnd}{subDirectoryForOutput}"
onlineURLForImages = 'https://s3.ap-southeast-1.amazonaws.com/shashi-and-trisha-wedd.ing/'

sqlCall = 'SELECT face_id from faces WHERE faces.face_name LIKE \"%blob%\"'
z = cur.execute(sqlCall)
result = z.fetchall()

for item in result:
	personID = item[0]

	sqlCall = f'SELECT face_name, face_URL FROM faces WHERE face_id = {personID}'
	z = cur.execute(sqlCall)
	result = z.fetchall()
	face_name = result[0][0]
	face_url = f"{result[0][1]}_tb-focused"
	print (f"building html for {face_name} to {face_url}" )

	myNewHeader = {"title": f"Photos of {face_name}", 
	"headline": f"{face_name}",
	"baseURLForFrontEnd": baseURLForFrontEnd,
	"baseURLForPhotos": baseURLForPhotos}


	template = env.get_template('single-person-album_thumb-focused_elit.jinja')

	outputHTML_filename = f'{face_url}.html'

	localURLForImages = dbs.basePathForPhotos

	theCall = f'''SELECT scaledPhotos.sourcePhoto_id, scaledPhotos.URL, facesInPhotos.face_id, faces.face_name, facesInPhotos.faceInPhoto_top_pc, facesInPhotos.faceInPhoto_left_pc
		FROM scaledPhotos 
		JOIN photos ON scaledPhotos.sourcePhoto_id = photos.photo_id 
		JOIN facesInPhotos ON photos.photo_id = facesInPhotos.photo_id 
		JOIN faces on faces.face_id = facesInPhotos.face_id 
		WHERE faces.face_id = {personID} and scaledPhotos.scaled_width = 500 
		ORDER BY ((facesInPhotos.faceInPhoto_right_abs - facesInPhotos.faceInPhoto_left_abs) * (facesInPhotos.faceInPhoto_bottom_abs - facesInPhotos.faceInPhoto_top_abs)) DESC'''

	sqlCall = theCall
	z = cur.execute(sqlCall)
	photoList = z.fetchall()


	photoListInDict = []
	for index, photo in enumerate(photoList):
		smallPhotoURL = photo[1]
		faceTop = int(photo[4] * 100)
		faceLeft = int(photo[5] * 100)
		sqlCall = f"SELECT scaledPhotos.URL FROM scaledPhotos WHERE scaledPhotos.sourcePhoto_id = {photo[0]} AND scaledPhotos.scaled_width = 1200"
		z = cur.execute(sqlCall)
		result = z.fetchall()
		if result:
			bigPhotoURL = result[0][0]
		else:
			bigPhotoURL = smallPhotoURL
		photoListInDict += [{'smallurl': smallPhotoURL,
		'bigurl': bigPhotoURL,
		'bindex': index, 
		'tnXPos': faceLeft,
		'tnYPos': faceTop}]


	# rendering the template and storing the resultant text in variable output
	output = template.render(headerstuff = myNewHeader, picList = photoListInDict)

	# printing the output on screen
	# print(output)
	filename_withFullPath = f"{outputDirectory_full}{outputHTML_filename}"
	filePath_full = os.path.split(filename_withFullPath)[0]
	os.makedirs(filePath_full, exist_ok = True)

	with open(f"{filename_withFullPath}", 'w') as f:
	    print(output, file = f)