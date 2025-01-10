import sqlite3

con = sqlite3.connect('wedding-album.db')
cur = con.cursor()

cur.execute('PRAGMA foreign_keys = YES')
z = cur.execute('PRAGMA foreign_keys')
print (f"Pragma foreign_keys is set to {z.fetchall()}")

cur.execute('''CREATE TABLE IF NOT EXISTS events (
	event_id INTEGER PRIMARY KEY, 
	event_name VARCHAR(255) UNIQUE NOT NULL,
	event_URL VARCHAR(255) UNIQUE NOT NULL)
''')

cur.execute('''CREATE TABLE IF NOT EXISTS faces (
	face_id INTEGER PRIMARY KEY,
	face_name VARCHAR(255) UNIQUE NOT NULL,
	face_URL VARCHAR(255) UNIQUE NOT NULL)
''')

cur.execute('''CREATE TABLE IF NOT EXISTS photos (
	photo_id INTEGER PRIMARY KEY,
	photo_filename VARCHAR(255) UNIQUE NOT NULL,
	event_id INT,
	FOREIGN KEY (event_id) REFERENCES events(event_id))
''')

cur.execute('''CREATE TABLE IF NOT EXISTS facesInPhotos(
	faceInPhoto_id INTEGER PRIMARY KEY,
	face_id INT,
	photo_id INT,
	faceInPhoto_left REAL,
	faceInPhoto_right REAL,
	faceInPhoto_top REAL,
	faceInPhoto_bottom REAL,
	match_distance REAL,
	FOREIGN KEY (face_id) REFERENCES faces(face_id),
	FOREIGN KEY (photo_id) REFERENCES photos(photo_id))
''')

con.commit()
con.close()