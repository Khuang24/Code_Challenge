import bs4 as bs
import MySQLdb
import requests


 
r = requests.get("https://rarbg.to/top100.php?category[]=14&category[]=15&category[]=16&category[]=17&category[]=21&category[]=22&category[]=42&category[]=44&category[]=45&category[]=46&category[]=47&category[]=48")

scrap_data = bs.BeautifulSoup(r.text,'hmtl')


db = MySQLdb.connect(host='localhost',    
                     user='root',        
                     passwd='password',  
                     db='moviedb')  

cursor = db.cursor()

for movie in scrap_data.find_all('tr',{'class':'lista2'}):


    name_id_info = movie.find_all('a')
   
    # Torrent Name
    torrent_name =  name_id_info[1].text
   
    # TMDB ID
    if len(name_id_info) >= 3 and "imdb" in name_id_info[2]["href"] :
        IMDB_id = str(name_id_info[2]["href"]).replace("https://rarbg.to/torrents.php?imdb=","")
    else:
        IMDB_id = ""
   
    torrent_info = movie.find_all('td',{'class':'lista'})    
   
    # Torrent Size
    torrent_size = torrent_info[3].text
   
    # Torrent Seeders
    torrent_seeders = torrent_info[4].text
    
    # Torrent Leechers        
    torrent_leechers= torrent_info[5].text

    cursor.execute("""INSERT INTO Top100Torrent(torrent_name, IMDB_id, torrent_size, torrent_seeders, torrent_leechers)
                   VALUES ('%s', '%s','%s',%d,%d)""" % (torrent_name,IMDB_id,torrent_size,int(torrent_seeders),int(torrent_leechers)))
  

db.commit()

