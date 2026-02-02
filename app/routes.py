from flask import Blueprint, render_template
from .models import Song
from .models.db import db



main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():

    songs = Song.query.limit(5).all()
    print(songs)

    return render_template('index.html')

