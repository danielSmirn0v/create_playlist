
from playlist_app import app

from flask import Flask, render_template, request, redirect, session, flash

from playlist_app.models import songs_in_playlist, user, playlist_name


@app.route('/playlist/<int:id>/new_playlist')
def new_playlist_page(id):

    if 'user_info' not in session:
        return redirect ('/')



    return render_template('new_playlist.html',user = user.User.get_one_by_id({'id': session['user_info']}), play = playlist_name.Playlist_name.get_all_playlists_by_user({'id':id}))

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
def add_song_page(id):
    print(f'hellow world{id}')
    if 'user_info' not in session:
        return redirect ('/')

    return render_template('add_to_playlist.html', user = user.User.get_one_by_id({'id': session['user_info']}), play = playlist_name.Playlist_name.get_one_by_user({'id':id}))

@app.route('/playlist/<int:id>/add_to_playlist/create', methods = ['POST'] )
def add_song_to_playlist(id):

    if 'user_info' not in session:
        return redirect ('/')

    print(f'{id}  ===')
    data = {
        'track_name' :request.form['track_name'],
        'artist_name' :request.form['artist_name'],
        'playlist_name_id' : id
##no idea how to insert this into table, a playlists content might be a perfect play fro class associsation, or vie versa, aplaylist is a perfect one ofr trakc ansd artists
    }
    print(f'{data}')
    songs_in_playlist.Playlist.save(data)
    
    return redirect('/playlist/dashboard') ##this is just to sample the redirt works


@app.route('/playlist/<int:id>/edit_playlist')
def edit_playlist(id):
    pass

@app.route('/playlist/<int:id>/delete_playlist')
def delete_playlist(id):
    pass
