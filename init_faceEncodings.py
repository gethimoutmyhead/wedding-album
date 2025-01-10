import face_recognition
import glob

testImagesDirectoryList = glob.glob('test_image/*.jpg')

for imagePath in testImagesDirectoryList:
	print ('Loading ' + imagePath)
	image = face_recognition.load_image_file(imagePath)

	
