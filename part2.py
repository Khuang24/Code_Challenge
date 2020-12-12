import bs4 as bs
import MySQLdb
import requests
import json

db = MySQLdb.connect(host='localhost',    
                     user='root',        
                     passwd='password',  
                     db='moviedb')  

cursor = db.cursor()

cursor.execute("Select imdb_id from top100torrent")
results = cursor.fetchall()

for movie in results:
	r = requests.get("https://api.themoviedb.org/3/movie/"+movie[0]+"?api_key=13ddcd553d3d51369cd6dbf7aceb8b75&language=en-US")

	movie_Data = json.loads(r.text)

	 # TMDB id, title, keywords
	movie_title = str(movie_Data["title"]).replace("'","''")
	movie_imdb_id = movie_Data["imdb_id"]
	movie_keywords = None;
	
	r = requests.get("https://api.themoviedb.org/3/movie/"+movie[0]+"/keywords?api_key=13ddcd553d3d51369cd6dbf7aceb8b75")
	keywords_Data = json.loads(r.text)
	movie_keywords = None
	
	for keyword in keywords_Data["keywords"]:	
		if movie_keywords == None:
			movie_keywords = keyword["name"]
		else:
			movie_keywords = movie_keywords + ", " + keyword["name"]
            
	movie_keywords = str(movie_keywords).replace("'","''")
	
	# Unique Only
	cursor.execute("""INSERT INTO themoviedb(IMDB_id, title, keywords)
				   VALUES ('%s', '%s','%s') ON DUPLICATE KEY UPDATE keywords = keywords""" % (movie_imdb_id, movie_title, movie_keywords))
	'''
	# Allows Duplicates	
	cursor.execute("""INSERT INTO themoviedb(IMDB_id, title, keywords)
				   VALUES ('%s', '%s','%s')""" % (movie_imdb_id, movie_title, movie_keywords))
	'''
db.commit()
