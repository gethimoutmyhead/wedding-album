import sqlite3
import main_dbsettings as db_settings
from slugify import slugify

con = sqlite3.connect(db_settings.photoAlbum_DB)
cur = con.cursor()

cur.execute('PRAGMA foreign_keys = ON')

sqlCall = '''SELECT facesInPhotos.face_id, faces.face_name, COUNT(facesInPhotos.faceInPhoto_id)
			FROM facesInPhotos 
			JOIN faces ON facesInPhotos.face_id = faces.face_id 
			GROUP BY facesInPhotos.face_id
			ORDER BY COUNT(facesInPhotos.faceInPhoto_id) DESC'''

z = cur.execute(sqlCall)
result = z.fetchall()
facesByPhotoCount = result


for face in facesByPhotoCount:

	faceID = face[0]
	faceName = face[1]
	photosWithFace_count= face[2]
	print (f"Face {faceID} - {faceName} has {photosWithFace_count} photos found")

	newname = input ("What is their name (blank if unknown or name correct), _exit to end script:")

	if (newname == '_exit'):
		exit()

	if newname:
		sqlCall = f'''SELECT face_id, face_name FROM faces WHERE face_name = \'{newname}\' '''
		z = cur.execute(sqlCall)
		result = z.fetchall()
		faceNameSearch = result
		if faceNameSearch:
			found_faceIdx = faceNameSearch[0][0]
			found_faceName = faceNameSearch[0][1]
			sqlCall = f'''SELECT COUNT(faceInPhoto_id) 
						FROM facesInPhotos 
						WHERE face_id = {found_faceIdx}'''

			z = cur.execute(sqlCall)
			result = z.fetchall()
			photosWithFoundFace_count = result[0][0]
			updateFaces = input (f'{found_faceName} is in db previously, on index {found_faceIdx}, with {photosWithFoundFace_count} images. Y to merge, empty or any other key to skip:')
			if (updateFaces == 'Y'):
				# print(f"existing name is on index {faceNameSearch[0][0]}")
				sqlCall = f'''UPDATE facesInPhotos
							SET face_id = {found_faceIdx}
							WHERE face_id = {faceID}'''
				z = cur.execute(sqlCall)
		else:
			print ('this name is not yet in the db. Updating name on database')
			newname_url = slugify(newname)
			sqlCall = f'''UPDATE faces 
						SET face_name = \'{newname}\', face_URL = \'{newname_url}\' 
						WHERE face_id = {faceID}'''
			z = cur.execute(sqlCall)
			con.commit()
	else:
		print ('skipped this face')
