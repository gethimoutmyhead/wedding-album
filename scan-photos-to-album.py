import numpy
import face_recognition as fr
import pickle
import glob
from PIL import Image
import sqlite3
from slugify import slugify

basePathForPhotos = '/Users/Shared/wedding stuff/Photos/'
encodedFacesDBPath = 'test_encoded-faces.dat'
photoAlbum_DB = 'test_wedding-album.db'
faceDistance_tolerance = 0.5

with open(encodedFacesDBPath, 'rb') as f:
    encodedFacesDB = pickle.load(f)

print (f"{len(encodedFacesDB)} unique faces on database")

con = sqlite3.connect(photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

z = cur.execute('SELECT face_id FROM faces')
g = z.fetchall()
if len(encodedFacesDB) != len(g):
	print (f'mismatch between face count on file: {len(encodedFacesDB)} and on SQLDB: {len(g)}')
	print ('exiting')
	exit()

## get user input for the directory to get images from
directoryOptions = glob.glob(f"{basePathForPhotos}*")
directoryIndexCount=0
for option in directoryOptions:
	print (f"{directoryIndexCount}. {option}\n")
	directoryIndexCount +=1
directoryIndexChosen = int(input("choose a directory: "))


searchPath = f"{directoryOptions[directoryIndexChosen]}/"
imagesInFolder = glob.glob(f"{searchPath}*.jpg")
imagesInFolder += glob.glob(f"{searchPath}*.jpeg")
print (f'{len(imagesInFolder)} found')

directoryPath_split = directoryOptions[directoryIndexChosen].split('/')

event_name = directoryPath_split[-1]
event_URL = slugify(event_name)
print (f'checking if {event_name} is in database')

sqlCall = f"SELECT * FROM events WHERE event_name = \'{event_name}\' OR event_URL = \'{event_URL}\'"
z = cur.execute(sqlCall)
result = z.fetchall() 

if not result:
	sqlCall = f"INSERT INTO events (event_name, event_URL) VALUES (\'{event_name}\', \'{event_URL}\')"
	cur.execute(sqlCall)
	sqlCall = f"SELECT * FROM events WHERE event_name = \'{event_name}\' OR event_URL = \'{event_URL}\'"
	z = cur.execute(sqlCall)
	result = z.fetchall()

event_index = result[0][0]

for testImage_path in imagesInFolder:

	testImage_path_split = testImage_path.split('/')
	testImage_URL = f"{testImage_path_split[-2]}/{testImage_path_split[-1]}"
	print (f"generated URL {testImage_URL} for image. Inserting to database")

	sqlCall = f"INSERT INTO photos (photo_filename, event_id) VALUES (\'{testImage_URL}\', {event_index})"
	cur.execute(sqlCall)
	con.commit()

	photoIndex = cur.lastrowid

	testImage = fr.load_image_file(testImage_path)
	testImage_faceLocations = fr.face_locations(testImage)
	testImage_faceEncodings = fr.face_encodings(testImage, known_face_locations = testImage_faceLocations, model='large')
	print (f"{len(testImage_faceEncodings)} faces found in image")
	

	'''
	print ('exporting cutouts of faces from image')
	faceIndex = 0
	while faceIndex < len(testImage_faceLocations):
		top, right, bottom, left = testImage_faceLocations[faceIndex]	
		face_image = testImage[top:bottom, left:right]
		pil_image = Image.fromarray(face_image)
		print (f'exporting test_portrait/extract_{faceIndex}.jpg')
		pil_image.save(f'test_portrait/extract_{faceIndex}.jpg')
		faceIndex +=1
	'''
	if (len(testImage_faceEncodings) == 0):
		print ('moving to next image')
	else:
		facesInImage_list = []

		for faceIndex, face in enumerate(testImage_faceLocations):
			facesInImage_list.append({'index': faceIndex, 'matchedToDB_index': -1, 'match_distance': 1.0})

		isLoopComplete=False
		faceCheck_index=0
		faceTestList = numpy.arange(0, len(encodedFacesDB))
		while isLoopComplete is False :

			testFaceFromDB_index = faceTestList[faceCheck_index]
			faceEncoding_toTest = encodedFacesDB[testFaceFromDB_index]
			print (f"testing database face {faceTestList[faceCheck_index]} against the image")

			faceDistanceVsTestImage = fr.face_distance(testImage_faceEncodings, faceEncoding_toTest)
			indexOfClosestMatch = faceDistanceVsTestImage.argmin()


			print ( f"DB index {testFaceFromDB_index} looks closest to image no. {indexOfClosestMatch}, distance: {faceDistanceVsTestImage[indexOfClosestMatch]}")
			print ( f"Image no. {indexOfClosestMatch} is currently matched to {facesInImage_list[indexOfClosestMatch]['matchedToDB_index']}, distance: {facesInImage_list[indexOfClosestMatch]['match_distance']}")

			if(faceDistanceVsTestImage[indexOfClosestMatch] < facesInImage_list[indexOfClosestMatch]['match_distance']):
				priorMatchIndex = facesInImage_list[indexOfClosestMatch]['matchedToDB_index']
				facesInImage_list[indexOfClosestMatch]['matchedToDB_index'] = testFaceFromDB_index
				facesInImage_list[indexOfClosestMatch]['match_distance'] = faceDistanceVsTestImage[indexOfClosestMatch]
			
				print ( f"updating to the new match")
				if (priorMatchIndex != -1):
					faceTestList = numpy.append(faceTestList, priorMatchIndex)
					print ( f"pushing DB image {priorMatchIndex} to bottom of the list for a re-match")
			faceCheck_index +=1
			if (len(faceTestList) == faceCheck_index):
				isLoopComplete = True

	
		for elem in facesInImage_list:
			if (elem['match_distance'] > faceDistance_tolerance):
				## the face does not closely match any existing faces, so its probably not known to db
				## add the face to the DB
				print ('new face was detected')
				encodedFacesDB.append(testImage_faceEncodings[elem['index']])
				latestIndex = len(encodedFacesDB) - 1
				elem['matchedToDB_index'] = latestIndex
				elem['match_distance'] = 0
				personNumString = "{:04d}".format(latestIndex)
				personName = f"person_{personNumString}"
				personURL = slugify(personName)
				print ('adding new face to DB')
				sqlCall = f"INSERT INTO faces (face_id, face_name, face_url) VALUES ({latestIndex},\'{personName}\',\'{personURL}\')"
				cur.execute(sqlCall)
				z = con.commit()

				print ('exporting cutout of new face')
				top, right, bottom, left = testImage_faceLocations[elem['index']]	
				face_image = testImage[top:bottom, left:right]
				pil_image = Image.fromarray(face_image)
				print (f'exporting test_portrait/cutout_{latestIndex}.jpg')
				pil_image.save(f'test_portrait/cutout_{latestIndex}.jpg')


			top, right, bottom, left = testImage_faceLocations[elem['index']]
			sqlCall = f'''INSERT INTO facesInPhotos (face_id, photo_id, faceInPhoto_left, faceInPhoto_right, faceInPhoto_top, faceInPhoto_bottom, match_distance) VALUES
							({elem['matchedToDB_index']},
							{photoIndex},
							{left},{right},{top},{bottom},
							{elem['match_distance']})'''
			cur.execute(sqlCall)
			z = con.commit()

with open(encodedFacesDBPath, 'wb') as f:
    pickle.dump(encodedFacesDB, f)

con.close()