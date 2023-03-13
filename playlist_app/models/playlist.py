
from playlist_app.config.mysqlconnection import connectToMySQL

from flask import flash

from playlist_app.models import user


class Playlist:
    db = 'playlist_creater'

    def __init__(self,data):
        self.id = data['id']
        self.playlist_name = data['playlist_name']
        self.track_name = data['track_name']
        self.artist_name = data['artist_name']
        self.user_id = data['user_id']
        self.all_playlist = []
        self.creater = None
        # self.likes = []

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO playlists (user_id, playlist_name, track_name, artist_name) VALUES(%(user_id)s,%(playlist_name)s, %(track_name)s,%(artist_name)s)'
        result = connectToMySQL(cls.db).query_db(query, data)
        print (result)
        return result

    @classmethod        #    SELECT * FROM sighting LEFT JOIN users ON sighting.user_id = users.id WHERE sighting.id = %(id)s
    def get_all(cls):
        query = 'SELECT * FROM playlists LEFT JOIN users ON playlists.user_id = users.id'
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
        query="SELECT * FROM playlists LEFT JOIN likes ON playlists.id = likes.playlist_id LEFT JOIN users ON likes.user_id = users.id WHERE id=%(id)s;"
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