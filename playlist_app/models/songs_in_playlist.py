
from playlist_app.config.mysqlconnection import connectToMySQL

from flask import flash

from playlist_app.models import user, playlist_name


class Playlist:
    db = 'playlist_creater'

    def __init__(self,data):
        self.id = data['id']
        self.track_name = data['track_name']
        self.artist_name = data['artist_name']
        self.playlist_name_id = data['playlist_name_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.all_tracks_in_playlists = []
        self.creater = None
        
    @classmethod
    def save(cls,data):
        query = 'INSERT INTO track (playlist_name_id, track_name, artist_name) VALUES(%(playlist_name_id)s,%(track_name)s,%(artist_name)s)' ##this mgiht have to be re-worked to inserte track name and artist into playlist_name
        result = connectToMySQL(cls.db).query_db(query, data)
        print (result)
        return result


    @classmethod
    def get_all_track_in_playlist(cls,data):
        query="""SELECT * FROM track WHERE playlist_name_id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results

#SELECT * FROM playlist_contents LEFT JOIN playlists_name ON playlist_contents.= playlists_name.id #SELECT * FROM track JOIN playlists_name ON track.playlist_name_id = playlists_name.id WHERE playlist_name_id = %(id)s
    @classmethod        
    def get_all_songs_in_playlist(cls,data): 
        print('about to run get all songs in query')
        query = '''SELECT * FROM track
                    JOIN playlists_name ON track.playlist_name_id = playlists_name.id
                    WHERE playlists_name.id = %(id)s''' 
        results = connectToMySQL(cls.db).query_db(query,data)
        print (f'{len(results)} results returned')
        all_tracks_in_playlists = []
        for row in results:
            if row['user_id'] == None:
                break
            playlist_data = {
                "id": row['playlists_name.id'],
                "playlist_name": row['playlist_name'],
                'user_id' : row['user_id'],
                "created_at": row['playlists_name.created_at'],
                "updated_at": row['playlists_name.updated_at']
            }
            this_playlist = cls(row)
            this_playlist.creater = playlist_name.Playlist_name(playlist_data)
            all_tracks_in_playlists.append(this_playlist)
            print(f'{this_playlist}this is the creater')
            print(f'{results}=====ksdw===')
        print(f'{len(all_tracks_in_playlists)} tracks in playlists')
        return all_tracks_in_playlists    

    @classmethod
    def update(cls,data):
        query="UPDATE track SET track_name=%(track_name)s, artist_name=%(artist_name)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def delete_song(cls,data):
        query = 'DELETE FROM track WHERE id = %(id)s'
        result  = connectToMySQL(cls.db).query_db(query,data)
        return result

    @staticmethod
    def validate_track(track):
        is_valid = True
        if len(track['track_name']) < 2:
            flash("Track name must be at least 2 characters long.")
            is_valid = False
        if len(track['artist_name']) < 2:
            flash("Artist must be at least 2 characters long.")
            is_valid = False
        return is_valid 
