
from playlist_app import app

from flask import Flask, render_template, request, redirect, session, flash

from playlist_app.models import playlist, user


@app.route('/playlist/<int:id>/new_playlist')
def new_playlist(id):
    pass

@app.route('/playlist/<int:id>/list_playlist')
def view_user_all_playlists(id):
    pass

@app.route('/playlist/<int:id>/add_to_playlist')
def add_song_to_playlist(id):
    pass

@app.route('/playlist/<int:id>/edit_playlist')
def edit_playlist(id):
    pass

@app.route('/playlist/<int:id>/delete_playlist')
def delete_playlist(id):
    pass
