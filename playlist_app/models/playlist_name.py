
from playlist_app.config.mysqlconnection import connectToMySQL

from flask import flash

from playlist_app.models import user, playlist


class Playlist_name:
    db = 'playlist_creater'

    def __init__(self,data):
        self.id = data['id']
        self.playlist_name = data['playlist_name']
        self.user_id = data['user_id']
        self.playlist_content_id = data['playlist_content_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.all_playlist = []
        self.creater = None
##double check all the instance, then check save query.
    @classmethod
    def save(cls,data):
        query = 'INSERT INTO playlists_name (user_id, playlist_content_id, playlist_name) VALUES(%(user_id)s, %(playlist_content_id)s,%(playlist_name)s)' ##this mgiht have to be re-worked to inserte track name and artist into playlist_name
        result = connectToMySQL(cls.db).query_db(query, data)
        print (result)
        return result