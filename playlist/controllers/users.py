
from playlist import app

from flask import Flask, render_template, request, redirect, session, flash

from playlist.models import user


@app.route('/')
def check():
    return render_template('list_playlist_base.html')