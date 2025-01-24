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

personID = 245

sqlCall = f'''SELECT face_id from faces 
	WHERE face_id = {personID}'''
z = cur.execute(sqlCall)
result = z.fetchall()

for person in result:
	personID = person[0]
	sqlCall = f'SELECT face_name, face_URL FROM faces WHERE face_id = {personID}'
	z = cur.execute(sqlCall)
	result = z.fetchall()
	face_name = result[0][0]
	face_url = result[0][1]
	print (f"building html for {face_name} to {face_url}" )

	template = env.get_template('elit1.jinja')
	outputPath = 'test_static/'
	outputHTML_filename = f'{face_url}.html'

	onlineURLForImages = 'https://s3.ap-southeast-1.amazonaws.com/shashi-and-trisha-wedd.ing/'
	localURLForImages = dbs.basePathForPhotos

	imageOutputPath = onlineURLForImages

	theCall = f'''SELECT scaledPhotos.sourcePhoto_id, scaledPhotos.URL, facesInPhotos.face_id, faces.face_name 
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
	myNewHeader = {"title": f"Photos of {face_name}", "headline": f"{face_name}"}
	output = template.render(headerstuff = myNewHeader, picList = photoListInDict)

	# printing the output on screen
	# print(output)

	with open(f"{outputPath}{outputHTML_filename}", 'w') as f:
	    print(output, file = f)