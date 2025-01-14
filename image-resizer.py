from PIL import Image, ImageOps
import main_dbsettings as db_settings
import sqlite3
import os
import errno

basePathForPhotos = db_settings.basePathForPhotos
encodedFacesDBPath = db_settings.encodedFacesDBPath
photoAlbum_DB = db_settings.photoAlbum_DB

con = sqlite3.connect(photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')


'''
## get user input for the directory to get images from
directoryOptions = glob.glob(f"{basePathForPhotos}*")
directoryOptions = sorted(directoryOptions)

for index, option in enumerate(directoryOptions):
	print (f"{index}. {option}\n")
directoryIndexChosen = int(input("choose a directory: "))

if ((directoryIndexChosen >= len(directoryOptions)) or (directoryIndexChosen < 0)):
	print ('index out of range. exiting')
	exit()

searchPath = f"{directoryOptions[directoryIndexChosen]}/"
imagesInFolder = glob.glob(f"{searchPath}*.jpg")
imagesInFolder += glob.glob(f"{searchPath}*.jpeg")
print (f'{len(imagesInFolder)} found')
imagesInFolder = sorted(imagesInFolder)
directoryPath_split = directoryOptions[directoryIndexChosen].split('/')
'''
targetDimensions = [{'width': 500},{'width': 1200}]

sqlCall = 'SELECT event_id, event_name from events'
z = cur.execute(sqlCall)
eventsList = z.fetchall()
for event in eventsList:
	print (f"{event[0]}. {event[1]}")

eventIndex = input ('Choose an event to resize:')

sqlCall = f'SELECT photo_filename, photo_id from photos WHERE event_id = {eventIndex}'
z = cur.execute(sqlCall)

for elem in z.fetchall():
	sourcePhoto_filename = elem[0]
	sourcePhoto_id = elem[1]
	directory = f"{basePathForPhotos}{sourcePhoto_filename.split('/')[-2]}/scaled/"
	print (directory)
	os.makedirs(directory, exist_ok = True)

	fullImagefilePath = f"{basePathForPhotos}{sourcePhoto_filename}"
	print (fullImagefilePath)
	im = Image.open(f"{basePathForPhotos}{sourcePhoto_filename}")
	im = ImageOps.exif_transpose(im)
	width, height = im.size
	for dimension in targetDimensions:
		resizedWidth = dimension["width"]
		resizedHeight = int(height * (resizedWidth / width))
		newsize = (resizedWidth, resizedHeight)
		im_resized = im.resize(newsize)
		fileName = elem[0].split('/')[-1]
		fileNameWithoutExtension = fileName.split('.')[-2]
		exportName = f"{directory}{fileNameWithoutExtension}_{resizedWidth}x{resizedHeight}.jpg"
		
		print (f"exporting to {exportName}")
		im_resized.save(exportName)

		URL = f"{exportName.split('/')[-3]}/{exportName.split('/')[-2]}/{exportName.split('/')[-1]}"
		print (f"checking if {URL} is already in the database")

		sqlCall = f"SELECT scaledPhoto_id FROM scaledPhotos WHERE URL = \'{URL}\'"
		z = cur.execute(sqlCall)
		result = z.fetchall()
		if result:
			print ('image is already in database, no rows added')
		else:
			print ('adding image to DB')
			sqlCall = f'''INSERT INTO scaledPhotos 
				(sourcePhoto_id,URL,
				scaled_width, scaled_height,
				padded_width, padded_height,
				padding_left, padding_top)
				VALUES 
				({sourcePhoto_id},\'{URL}\',
				{resizedWidth}, {resizedHeight},
				{resizedWidth}, {resizedHeight},
				0,0)'''
			cur.execute(sqlCall)
			con.commit()

