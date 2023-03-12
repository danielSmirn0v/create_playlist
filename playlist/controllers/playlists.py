
from playlist import app

from flask import Flask, render_template, request, redirect, session, flash

from playlist.models import user, playlist


@app.route('playlist/<id:id>/new_playlist')
def new_playlist(id):
    pass

@app.route('playlist/<id:id>/list_playlist')
def view_user_all_playlists(id):
    pass

@app.route('playlist/<id:id>/add_to_playlist')
def add_song_to_playlist(id):
    pass

@app.route('playlist/<id:id>/edit_playlist')
def edit_playlist(id):
    pass

@app.route('playlist/<id:id>/delete_playlist')
def delete_playlist(id):
    pass
