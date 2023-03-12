
from playlist_app import app

from flask import Flask, render_template, request, redirect, session, flash

from playlist_app.models import playlist, user


@app.route('/playlist/<int:id>/new_playlist')
def new_playlist(id):

    if 'user_info' not in session:
        return redirect ('/')
    data = {
        'playlist_name' : request.form['playlist_name']
    }
    playlist_name = playlist.Playlist.save(data)
    print(playlist_name)
    return render_template('new_playlist.html')

@app.route('/playlist/create/<int:id>/new_playlist', methods = ['POST'])
def new_playlist(id):

    if 'user_info' not in session:
        return redirect ('/')
    data = {
        'playlist_name' : request.form['playlist_name']
    }
    playlist_name = playlist.Playlist.save(data)
    print(playlist_name)
    return redirect('/playlist/user/<int:id>/all_playlists')

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
