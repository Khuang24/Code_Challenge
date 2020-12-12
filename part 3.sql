CREATE TABLE joined_table as 
SELECT t.id, t.torrent_name, t.IMDB_id, t.torrent_size, t.torrent_seeders, t.torrent_leechers, m.title, m.keywords FROM Top100Torrent t
JOIN themoviedb m ON t.IMDB_id = m.IMDB_id
