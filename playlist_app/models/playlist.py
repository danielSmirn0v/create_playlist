
from playlist_app.config.mysqlconnection import connectToMySQL

from flask import flash

from playlist_app.models import user


class Playlist:
    db = 'playlist_creater'

    def __init__(self,data):
        self.id = data['id']
        self.track_name = data['track_name']
        self.artist_name = data['artist_name']
        self.user_id = data['user_id']
        self.all_playlist = []
        self.creater = None
        # self.likes = []
    ##this instance should be good, after editing the save query check if it works
    @classmethod
    def save(cls,data):
        query = 'INSERT INTO playlists (user_id, playlist_name, track_name, artist_name) VALUES(%(user_id)s,%(playlist_name)s, %(track_name)s,%(artist_name)s)' ##this mgiht have to be re-worked to inserte track name and artist into playlist_name
        result = connectToMySQL(cls.db).query_db(query, data)
        print (result)
        return result

    @classmethod        #    SELECT * FROM sighting LEFT JOIN users ON sighting.user_id = users.id WHERE sighting.id = %(id)s
    def get_all(cls):
        query = 'SELECT * FROM playlist_contents LEFT JOIN playlists_name ON playlist_contents.user_id = playlists_name.user_id LEFT JOIN users ON playlists_name.user_id = users.id' ##this query should work, it didnt goive an error in the terminal
        results = connectToMySQL(cls.db).query_db(query)
        print (f'{results} this is results')
        all_playlists = []
        for row in results:
            this_playlist = cls(row)
            data={
                'id':row['users.id'],
                'username':row['username'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':"",
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at'],
            }
            this_playlist.creater= user.User(data)
            all_playlists.append(this_playlist)
            print('=======')
            print(f'{all_playlists} this is alll')
        return all_playlists

    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM playlists LEFT JOIN users ON playlists.user_id = users.id WHERE playlists.id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def update(cls,data):
        query="UPDATE playlists SET playlist_name=%(playlist_name)s, track_name=%(track_name)s, artist_name=%(artist_name)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM playlists WHERE id = %(id)s'
        result  = connectToMySQL(cls.db).query_db(query,data)
        return result

    @staticmethod
    def validate_playlist(playlist):
        is_valid = True
        if len(playlist['playlist_name']) < 2:
            flash("Name must be at least 2 characters long.")
            is_valid = False
        return is_valid 