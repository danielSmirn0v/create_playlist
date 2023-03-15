
from playlist_app.config.mysqlconnection import connectToMySQL

from flask import flash

from playlist_app.models import user, playlist


class Playlist_name:
    db = 'playlist_creater'

    def __init__(self,data):
        self.id = data['id']
        self.playlist_name = data['playlist_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.all_playlist = []
        self.creater = None
##double check all the instance, then check save query.
    @classmethod
    def save(cls,data):
        query = 'INSERT INTO playlists_name (user_id, playlist_name) VALUES(%(user_id)s, %(playlist_name)s)' ##this mgiht have to be re-worked to inserte track name and artist into playlist_name
        result = connectToMySQL(cls.db).query_db(query, data)
        print (result)
        return result

    @classmethod
    def get_all_playlists_by_user(cls,data):
        query="SELECT * FROM playlists_name LEFT JOIN users ON playlists_name.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
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




    @staticmethod
    def validate_playlist(playlist):
        is_valid = True
        if len(playlist['playlist_name']) < 2:
            flash("Name must be at least 2 characters long.")
            is_valid = False
        return is_valid 