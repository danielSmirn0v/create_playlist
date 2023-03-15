
from playlist_app import app

from flask import Flask, render_template, request, redirect, session, flash

from playlist_app.models import playlist, user, playlist_name


@app.route('/playlist/<int:id>/new_playlist')
def new_playlist_page(id):

    if 'user_info' not in session:
        return redirect ('/')



    return render_template('new_playlist.html',user = user.User.get_one_by_id({'id': session['user_info']}))

@app.route('/playlist/<int:id>/new_playlist/create', methods = ['POST'])
def new_playlist(id):

    if 'user_info' not in session:
        return redirect ('/')
    data = {
        'playlist_name' : request.form['playlist_name'],
        'user_id' : session['user_info']
    }
    p_name = playlist_name.Playlist_name.save(data)
    print(f'{p_name} yoooowhast')
    return redirect(f'/playlist/user/{id}/all_playlists')

# @app.route('/playlist/<int:id>/list_playlist')
# def view_user_genre_playlists(id):

#     if 'user_info' not in session:
#         return redirect ('/')
#     return render_template('user_single_playlist_list.html',user = user.User.get_one_by_id({'id': session['user_info']}) )
#     pass

@app.route('/playlist/<int:id>/add_to_playlist')
def add_song_to_playlist(id):
    if 'user_info' not in session:
        return redirect ('/')

    data = {
        'track_name' :request.form['track_name'],
        'artist_name' :request.form['artist_name'],
        'user_id' :session['user_info']
    }

    pass

@app.route('/playlist/<int:id>/edit_playlist')
def edit_playlist(id):
    pass

@app.route('/playlist/<int:id>/delete_playlist')
def delete_playlist(id):
    pass
