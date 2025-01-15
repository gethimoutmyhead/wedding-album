sqlCall = '''SELECT scaledPhotos.scaledPhoto_id, scaledPhotos.URL, facesInPhotos.face_id, faces.face_name 
	FROM scaledPhotos 
	JOIN photos ON scaledPhotos.sourcePhoto_id = photos.photo_id 
	JOIN facesInPhotos ON photos.photo_id = facesInPhotos.photo_id 
	JOIN faces on faces.face_id = facesInPhotos.face_id 
	WHERE faces.face_name LIKE \'%Kier%\''''