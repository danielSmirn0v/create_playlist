
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
        query="SELECT * FROM playlists_name WHERE playlists_name.user_id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
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
#SELECT * FROM playlist_contents LEFT JOIN playlists_name ON playlist_contents.= playlists_name.id
    @classmethod        #SELECT * FROM track JOIN playlists_name ON track.playlist_name_id = playlists_name.id WHERE playlist_name_id = %(id)s
    def get_all_songs_in_playlist(cls,data): 
        print('about to run get all songs in query')
        query = '''SELECT * FROM track
                    JOIN playlists_name ON track.playlist_name_id = playlists_name.id
                    WHERE playlist_name_id = %(id)s''' 
        results = connectToMySQL(cls.db).query_db(query,data)
        print (f'{results} results returned')
        all_tracks_in_playlists = []
        for row in results:
            this_song = cls(row)
            playlist_data = {
                "id": row['playlists_name.id'],
                "playlist_name": row['playlist_name'],
                'user_id' : data['user_id'],
                "created_at": row['playlists_name.created_at'],
                "updated_at": row['playlists_name.updated_at']
            }
            this_song.creater = Playlist_name(playlist_data)
            all_tracks_in_playlists.append(this_song)
            print(f'{all_tracks_in_playlists}=====ksdw===')

        # song = Playlist_name.all_songs_playlist(row)
        # if song:
        #     song_in_playlist.append(song)
        # for row in results:

                
            # if row['user_id'] == None:
            #     break



            # song_in_playlist.append(Playlist_name.all_songs_playlist(row))
        print(f'{results} this is the reulst')
        return results        ##figure out why this Playlist object is not iterable




    @staticmethod
    def validate_playlist(playlist):
        is_valid = True
        if len(playlist['playlist_name']) < 2:
            flash("Name must be at least 2 characters long.")
            is_valid = False
        return is_valid 