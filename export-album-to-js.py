import sqlite3
import main_dbsettings as dbs
import json
con = sqlite3.connect(dbs.photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

sqlCall = '''SELECT scaledPhotos.sourcePhoto_id, scaledPhotos.URL, photos.event_ID 
	from scaledPhotos
	JOIN photos ON scaledPhotos.sourcePhoto_id = photos.photo_id
	WHERE scaledPhotos.scaled_width = 1200 AND photos.event_ID = 3'''
z = cur.execute(sqlCall)
photoList = z.fetchall()

photoListInDict = []
for index, photo in enumerate(photoList):
	fullURL = f"{dbs.basePathForPhotos}{photo[1]}"
	photoListInDict.append({'index': photo[0], 'URL': fullURL})

#print (photoListInDict)

photoListInJSON = json.dumps(photoListInDict)
outputText = f"gallery = {photoListInJSON}"

with open('test_static/testAlbum.js', "w") as textfile:
	textfile.write(outputText)
