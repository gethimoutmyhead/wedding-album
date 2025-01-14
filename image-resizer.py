from PIL import Image
import glob
import test_dbsettings as db_settings
import sqlite3

basePathForPhotos = db_settings.basePathForPhotos
encodedFacesDBPath = db_settings.encodedFacesDBPath
photoAlbum_DB = db_settings.photoAlbum_DB

con = sqlite3.connect(photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

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
