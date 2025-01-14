import sqlite3
import test_dbsettings as dbs
import json
con = sqlite3.connect(dbs.photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

sqlCall = 'SELECT sourcePhoto_id, URL from scaledPhotos WHERE scaled_width = 500'
z = cur.execute(sqlCall)
photoList = z.fetchall()

photoListInDict = []
for index, photo in enumerate(photoList):
	fullURL = f"{dbs.basePathForPhotos}{photo[1]}"
	photoListInDict.append({'index': photo[0], 'URL': fullURL})

print (photoListInDict)

photoListInJSON = json.dumps(photoListInDict)
outputText = f"gallery = {photoListInJSON}"

with open('test_static/testAlbum.js', "w") as textfile:
	textfile.write(outputText)
