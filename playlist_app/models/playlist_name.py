
from playlist_app.config.mysqlconnection import connectToMySQL

from flask import flash

from playlist_app.models import songs_in_playlist, user


class Playlist_name:
    db = 'playlist_creater'

    def __init__(self,data):
        self.id = data['id']
        self.playlist_name = data['playlist_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.all_songs_playlist = []
        self.creater = None
##double check all the instance, then check save query.
    @classmethod
    def save(cls,data):
        query = 'INSERT INTO playlists_name (user_id, playlist_name) VALUES(%(user_id)s, %(playlist_name)s)' ##this mgiht have to be re-worked to inserte track name and artist into playlist_name
        result = connectToMySQL(cls.db).query_db(query, data)
        print (result)
        return result

    @classmethod
    def get_one_by_user(cls,data):
        query="SELECT * FROM playlists_name WHERE playlists_name.id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print(f'{result}==playkist')
        return result

    @classmethod
    def get_all_playlist(cls):
        query="SELECT * FROM playlists_name LEFT JOIN users ON playlists_name.user_id = users.id"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_playlists = []
        for row in results:
            this_playlist = cls(row)
            user_data = {
                "id": row['users.id'],
                "username": row['username'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_playlist.creater = user.User(user_data)
            all_playlists.append(this_playlist)
        return all_playlists




    @classmethod
    def get_all_playlists_by_user(cls,data):
        query="SELECT * FROM playlists_name JOIN users ON playlists_name.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        all_playlists = []
        for row in results:
            song_in_playlist = cls(row)
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
            song_in_playlist.creater= user.User(data)
            all_playlists.append(song_in_playlist)
            print('=======')
            print(f'{all_playlists} this is alll')
        return all_playlists
    ##figure out why this Playlist object is not iterable
##query = 'DELETE FROM playlists_name WHERE id = %(id)s'
    @classmethod
    def delete_playlist(cls,data):
        print('about to run delete query')
        track_query = 'DELETE FROM track WHERE playlist_name_id = %(id)s'
        result  = connectToMySQL(cls.db).query_db(track_query,data)
        playlist_query = 'DELETE FROM playlists_name WHERE id = %(id)s'
        playlist_result  = connectToMySQL(cls.db).query_db(playlist_query,data)
        print('ran delete')
        print(result)
        return playlist_result

    @classmethod
    def update_playlist(cls,data):
        query="UPDATE playlists_name SET playlist_name = %(playlist_name)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @staticmethod
    def validate_playlist(playlist):
        is_valid = True
        if len(playlist['playlist_name']) < 2:
            flash("Name must be at least 2 characters long.")
            is_valid = False
        return is_valid 