from flask import Blueprint, render_template, redirect, url_for, flash
from .models import Song
from .models.db import db
from .forms.disk_form import DiskForm
from .models.Disk import Disk
from .models.db import db



main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():

    songs = Song.query.limit(5).all()
    print(songs)

    return render_template('index.html')

@main_bp.route('/add-disk', methods=['GET', 'POST'])
def add_disk():
    form = DiskForm()
    if form.validate_on_submit():
        new_disk = Disk(
            name=form.name.data,
            company=form.company.data,
            size=form.size.data,
            sakisid=form.sakisid.data,
            notes=form.notes.data
        )
        db.session.add(new_disk)
        db.session.commit()
        flash('Disk added successfully!')
        return redirect(url_for('main.index'))
    return render_template('add_disk.html', form=form)

