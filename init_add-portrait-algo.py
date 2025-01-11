import face_recognition as fr
import glob
from PIL import Image
import pickle
import sqlite3

encodedFacesDBPath = 'wedding-album_encoded-faces.dat'
photoAlbum_DB = 'wedding-album.db'

con = sqlite3.connect(photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

PortraitDirectoryList = glob.glob('test_portrait/image_*.jpg')
PortraitDirectoryList += glob.glob('test_portrait/image_*.jpeg')
faceEncodingsDB = []
facesFoundIndex = 0
for image_path in PortraitDirectoryList:
	print ('loading ' + image_path)
	image = fr.load_image_file(image_path)

	print ('finding faces in ' + image_path)
	facesLocated = fr.face_locations(image)

	print (f"found {len(facesLocated)} faces. Encoding..")

	facesEncoded = fr.face_encodings(image, known_face_locations = facesLocated, model='large')

	for face in facesEncoded:
		faceEncodingsDB.append(face)

	if (facesLocated):
		for faceLocation in facesLocated:
			top, right, bottom, left = faceLocation		
			face_image = image[top:bottom, left:right]
			pil_image = Image.fromarray(face_image)
			pil_image.save(f"test_portrait/cutout_{facesFoundIndex}.jpg")
			print (f"exported test_portrait/cutout_{facesFoundIndex}.jpg")
			personNumString = "{:04d}".format(facesFoundIndex)
			personName = f"person_{personNumString}"
			print (f"adding to SQL table {personName}")
			cur.execute(f"INSERT INTO faces (face_id, face_name, face_url) VALUES ({facesFoundIndex},\'{personName}\',\'{personName}\')")
			z = con.commit()
			print(z)
			facesFoundIndex +=1


with open(encodedFacesDBPath, 'wb') as f:
    pickle.dump(faceEncodingsDB, f)

con.close()
