
from playlist import app

from flask import Flask, render_template, request, redirect, session, flash

from playlist.models import user, playlist

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def check():
    return render_template('register.html')

@app.route('/create', methods = ['POST'])
def register():

    if request.form['action'] == 'register':

        if not user.User.validate(request.form):
            return redirect('/')
        
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
        print(f'you got {user_info} in ')
        session['user_info'] = user_info
        print()

    else:


        print('wow we are here')
        user_info = user.User.get_onewith_email ({'email': request.form['email'].lower()})
        print("This is the user")
        print(user_info)
        if user_info:
            if len(request.form['password']) < 8:
                flash("Password must be at least 8 characters")
                return redirect("/")
            if bcrypt.check_password_hash(user_info.password, request.form['password']):
                session["user_info"] = user_info.id
                return redirect("/dashboard")
            else:
                flash("Incorrect Password")
                return redirect("/")
        else:
            flash("No user with this email")
            return redirect("/")



    return redirect('/dashboard')

@app.route('/dashboard')
def user_dash():

    if 'user_info' not in session:
        return redirect('/')

    print('wowow')
    return render_template('update_user_info.html', user = user.User.get_one_by_id({'id': session['user_info']})) ##dashabord html should be different

@app.route('/user/<id:id>/update')##route might neeed renaming?
def update_user(id):

    if 'user_info' not in session:
        return redirect('/')

    return redirect('list_playlist_in_session.html', user = user.User.get_one_by_id({'id': session['user_info']}))

@app.route('/user/<id:id>/update', methods = ['POST']) ##check to see if it work, might have to add some things in
def update_user(id):

    if 'user_info' not in session:
        return redirect('/')

    if not user.User.validate(request.form):
        return redirect(f'user/{id}/update')

    data={
            "id":id,
            "username":request.form["username"],
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],

    }

    user.User.update(data)

    return redirect('list_playlist_in_session.html') ##find a better place to re-route, maybe make a user info page