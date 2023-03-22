
from playlist_app import app

from flask import Flask, render_template, request, redirect, session, flash

from playlist_app.models import songs_in_playlist, user, playlist_name

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def check():
    
    return render_template('list_playlist.html', play = playlist_name.Playlist_name.get_all_playlist())

@app.route('/playlist/user/<int:id>/single_playlist_notin_session')
def single_playlist(id):


    return render_template('list_playlist_with_songs.html', pl_name = songs_in_playlist.Playlist.get_all_songs_in_playlist({'id':id}))

@app.route('/register')
def register_form():

    return render_template('register.html')

@app.route('/create', methods = ['POST'])
def register():

    if request.form['action'] == 'register':

        if not user.User.validate(request.form):
            return redirect('/register')
        
        username_exists = user.User.get_onewith_username({'username': request.form['username']})
        if username_exists:
            flash('username already used')
            return redirect('/')

        pw_hash = bcrypt.generate_password_hash(request.form["password"])

        data = {
            'username' : request.form['username'],
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password': pw_hash
        
        }

        user_info = user.User.save(data)

        session['user_info'] = user_info


    else:


        user_info = user.User.get_onewith_email ({'email': request.form['email'].lower()})
        print(user_info)
        if user_info:
            if len(request.form['password']) < 8:
                flash("Password must be at least 8 characters")
                return redirect("/")
            if bcrypt.check_password_hash(user_info.password, request.form['password']):
                session["user_info"] = user_info.id
                return redirect("/playlist/dashboard")
            else:
                flash("Incorrect Password")
                return redirect("/")
        else:
            flash("No user with this email")
            return redirect("/")



    return redirect('/playlist/dashboard')

@app.route('/playlist/dashboard')
def user_dash():

    if 'user_info' not in session:
        return redirect('/')

    print('wowow')
    return render_template('list_playlist_in_session.html', user = user.User.get_one_by_id({'id': session['user_info']}), play = playlist_name.Playlist_name.get_all_playlist()) ##dashabord html should be different



@app.route('/playlist/user/<int:id>/all_playlists')
def user_show_all_playlists(id):

    if 'user_info' not in session:
        return redirect('/')

    return render_template('user_playlists.html', play = playlist_name.Playlist_name.get_all_playlists_by_user({'id': session['user_info']}),user = user.User.get_one_by_id({'id': session['user_info']}))


@app.route('/playlist/user/<int:id>/single_playlist') ##working here rn
def user_single_playlist(id):

    if 'user_info' not in session:
        return redirect('/')

    return render_template('user_single_playlist_list.html', play = songs_in_playlist.Playlist.get_all_songs_in_playlist({'id':id}),user = user.User.get_one_by_id({'id': session['user_info']}),pl_name = playlist_name.Playlist_name.get_one_by_user({'id':id}))

@app.route('/playlist/user/<int:id>/update')
def update_user_page(id):

    if 'user_info' not in session:
        return redirect('/')
    print(id)

    return render_template('update_user_info.html', user = user.User.get_one_by_id({'id': session['user_info']}))

@app.route('/user/<int:id>/update', methods = ['POST']) ##update works
def update_user(id):

    if 'user_info' not in session:
        return redirect('/')

    if not user.User.validate_update_user(request.form):
        return redirect(f'/playlist/user/{id}/update')

    data={
            "id":id,
            "username":request.form["username"],
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],

    }

    user.User.update(data)

    return redirect('/playlist/dashboard') ##find a better place to re-route, maybe make a user info page

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
