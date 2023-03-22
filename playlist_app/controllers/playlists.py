
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
        
    if not playlist_name.Playlist_name.validate_playlist(request.form):
            return redirect(f'/playlist/{id}/new_playlist')
    data = {
        'playlist_name' : request.form['playlist_name'],
        'user_id' : session['user_info']
    }
    p_name = playlist_name.Playlist_name.save(data)
    print(f'{p_name} yoooowhast')
    return redirect(f'/playlist/user/{id}/all_playlists')

@app.route('/playlist/<int:id>/add_to_playlist')
def add_song_page(id):

    if 'user_info' not in session:
        return redirect ('/')

    return render_template('add_to_playlist.html', user = user.User.get_one_by_id({'id': session['user_info']}), play = playlist_name.Playlist_name.get_one_by_user({'id':id}))

@app.route('/playlist/<int:id>/add_to_playlist/create', methods = ['POST'] )
def add_song_to_playlist(id):

    if 'user_info' not in session:
        return redirect ('/')

    if not songs_in_playlist.Playlist.validate_track(request.form):
            return redirect(f'/playlist/{id}/add_to_playlist')

    print(f'{id}  ===')
    data = {
        'track_name' :request.form['track_name'],
        'artist_name' :request.form['artist_name'],
        'playlist_name_id' : id

    }

    songs_in_playlist.Playlist.save(data)
    
    return redirect(f'/playlist/user/{id}/single_playlist') 

@app.route('/playlist/<int:id>/update')
def update_playlist(id):

    if 'user_info' not in session:
        return redirect('/')

    return render_template('update_playlist_name.html', pl_name = playlist_name.Playlist_name.get_one_by_user({'id':id}), user = user.User.get_one_by_id({'id': session['user_info']}))

@app.route('/playlist/<int:id>/update/playlistname', methods = ['POST']) ##update works
def update_playlist_name(id):

    if 'user_info' not in session:
        return redirect('/')

    if not playlist_name.Playlist_name.validate_playlist(request.form):
        return redirect(f'/playlist/{id}/update')

    data={
            "id":id,
            "playlist_name": request.form['playlist_name'],
    }

    playlist_name.Playlist_name.update_playlist(data)

    return redirect(f"/playlist/user/{session['user_info']}/all_playlists")

@app.route('/playlist/<int:id>/delete_playlist')
def delete_playlist(id):

    if 'user_info' not in session:
        return redirect('/')

    playlist_name.Playlist_name.delete_playlist({'id': id})

    return redirect(f"/playlist/user/{session['user_info']}/all_playlists")

@app.route('/playlist/<int:id>/delete_song')
def delete_song(id):
    
    if 'user_info' not in session:
        return redirect('/')

    songs_in_playlist.Playlist.delete_song({'id': id})


    return redirect(f"/playlist/user/{session['user_info']}/all_playlists") #find a better way to reroute
