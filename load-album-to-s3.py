import boto3
import s3_bucket_details as s3db
s3 = boto3.resource(
    service_name=s3db.service_name,
    region_name=s3db.region_name,
    aws_access_key_id=s3db.aws_access_key_id,
    aws_secret_access_key=s3db.aws_secret_access_key
)
result = s3.buckets.all()
for index, bucket in enumerate(result):
	print (f"{index}. {bucket.name}")

bucketIndex_chosen = input ('choose a bucket')

# uploadBucket = result[bucketIndex_chosen].name
uploadBucket = s3db.s3bucket
'''
import pandas as pd

# Make dataframes
foo = pd.DataFrame({'x': [1, 2, 3], 'y': ['a', 'b', 'c']})
bar = pd.DataFrame({'x': [10, 20, 30], 'y': ['aa', 'bb', 'cc']})

# Save to csv
foo.to_csv('foo.csv')
bar.to_csv('bar.csv')

#s3.Bucket('theweddingalbumbucket').upload_file(Filename='foo.csv', Key='test/scaled/foo.csv')
#s3.Bucket('theweddingalbumbucket').upload_file(Filename='bar.csv', Key='bar.csv')
'''
import sqlite3
import main_dbsettings as dbs
con = sqlite3.connect(dbs.photoAlbum_DB)
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')

# sqlCall = '''SELECT scaledPhotos.sourcePhoto_id, scaledPhotos.URL, photos.event_ID 
# 	from scaledPhotos
# 	JOIN photos ON scaledPhotos.sourcePhoto_id = photos.photo_id
# 	WHERE scaledPhotos.scaled_width = 500 AND photos.event_ID = 3'''
sqlCall = '''SELECT scaledPhotos.scaledPhoto_id, scaledPhotos.URL, facesInPhotos.face_id, faces.face_name 
	FROM scaledPhotos 
	JOIN photos ON scaledPhotos.sourcePhoto_id = photos.photo_id 
	JOIN facesInPhotos ON photos.photo_id = facesInPhotos.photo_id 
	JOIN faces on faces.face_id = facesInPhotos.face_id 
	WHERE faces.face_id = 40'''
	
z = cur.execute(sqlCall)
results = z.fetchall()
for a in results:
	print (a[1])
	localPath = dbs.basePathForPhotos
	localFile = f"{localPath}{a[1]}"
	print (localFile)
	uploadPath = f'{a[1]}'
	print (uploadPath)
	s3.Bucket(uploadBucket).upload_file(Filename=localFile, Key=uploadPath)