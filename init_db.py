import sqlite3

con = sqlite3.connect('wedding_album.db')

cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS events (
	event_id INTEGER PRIMARY KEY, 
	event_name VARCHAR(255) UNIQUE NOT NULL,
	event_URL VARCHAR(255) UNIQUE NOT NULL)
''')

cur.execute('''CREATE TABLE IF NOT EXISTS photos (
	photo_id INTEGER PRIMARY KEY,
	photo_filename VARCHAR(255) NOT NULL,
	event_id INT REFERENCES events(event_id))
''')

cur.execute('''CREATE TABLE IF NOT EXISTS faces (
	face_id INTEGER PRIMARY KEY,
	face_name VARCHAR(255) UNIQUE NOT NULL,
	face_URL VARCHAR(255) UNIQUE NOT NULL)
''')

cur.execute('''CREATE TABLE IF NOT EXISTS facesInPhotos(
	faceInPhoto_id INT PRIMARY KEY,
	face_id INT REFERENCES faces(face_id),
	photo_id INT REFERENCES photos(photo_id),
	faceInPhoto_left REAL,
	faceInPhoto_right REAL,
	faceInPhoto_top REAL,
	faceInPhoto_bottom REAL)
''')

con.close()