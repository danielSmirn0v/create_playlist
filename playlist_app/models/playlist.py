
from playlist_app.config.mysqlconnection import connectToMySQL

from flask import flash

from playlist_app.models import user, playlist_name


class Playlist:
    db = 'playlist_creater'

    def __init__(self,data):
        self.id = data['id']
        self.track_name = data['track_name']
        self.artist_name = data['artist_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.playlist_name_id = data['playlist_name_id']
        self.all_songs_playlist = []
        
        # self.likes = []
    ##this instance should be good, after editing the save query check if it works
    @classmethod
    def save(cls,data):
        query = 'INSERT INTO playlists_contents (playlist_content_id, track_name, artist_name) VALUES(%(playlist_content_id)s, %(track_name)s,%(artist_name)s)' ##this mgiht have to be re-worked to inserte track name and artist into playlist_name
        result = connectToMySQL(cls.db).query_db(query, data)
        print (result)
        return result
#'SELECT * FROM playlist_contents LEFT JOIN playlists_name ON playlist_contents.playlist_name_id = playlists_name.id WHERE playlists_name.id = %()s'
##this query finally works all that was missing is 'id'
    @classmethod        
    def get_all_songs_in_playlist(cls,data): 
        print('about to run get all songs in query')
        query = 'SELECT * FROM playlist_contents LEFT JOIN playlists_name ON playlist_contents.playlist_name_id = playlists_name.id WHERE playlists_name.id = %(id)s' 
        results = connectToMySQL(cls.db).query_db(query,data)
        print (f'{results} this is results')
        if results:
            this_playlist = cls(results[0])
            for row in results:
                if row['user_id'] == None:
                    break

            this_playlist.all_songs_playlist.append(playlist_name.Playlist_name(row))
            return this_playlist
        print(this_playlist)
        return False ##figure out why this Playlist object is not iterable



    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM playlists_name LEFT JOIN users ON playlists_name.user_id = users.id WHERE playlists.id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def update(cls,data):
        query="UPDATE playlists_contents SET track_name=%(track_name)s, artist_name=%(artist_name)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM playlist_contents WHERE id = %(id)s'
        result  = connectToMySQL(cls.db).query_db(query,data)
        return result
